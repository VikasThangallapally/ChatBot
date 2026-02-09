"""
Image prediction endpoint for brain tumor MRI analysis.
Includes MRI image validation before running predictions.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from PIL import Image
from io import BytesIO
from app.services.inference import InferenceService
from app.schemas.prediction import PredictionResponse
from app.core.disclaimer import get_disclaimer
from app.dependencies import get_model_loader
from app.core.model_loader import ModelLoader
from app.config import settings
from app.core.auth import get_current_user
from app.utils.logger import get_logger
import os

logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict brain tumor from MRI image",
    description="Upload an MRI image and get prediction results with disclaimer"
)
async def predict(
    file: UploadFile = File(...),
    model_loader: ModelLoader = Depends(get_model_loader),
    current_user: dict = Depends(get_current_user)
):
    """
    Predict brain tumor presence from MRI image.
    
    Args:
        file: Uploaded MRI image file
        model_loader: Model loader dependency
        
    Returns:
        PredictionResponse: Prediction results with disclaimer
        
    Raises:
        HTTPException: If file validation fails or inference fails
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        if not file.content_type or "image" not in file.content_type:
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file contents
        file_contents = await file.read()
        
        if len(file_contents) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Save uploaded file
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file_contents)
        
        # Load image for validation
        try:
            image = Image.open(BytesIO(file_contents))
        except Exception as e:
            logger.error(f"Failed to open image: {str(e)}")
            return {
                "predictions": [],
                "top_prediction": None,
                "image_path": file_path,
                "model_version": None,
                "status": "invalid_image",
                "disclaimer": "⚠️ INVALID IMAGE: Could not read the uploaded file. Please ensure it's a valid image file (JPEG, PNG, etc.)",
                "is_valid_brain_image": False,
                "image_validation_confidence": 0.0,
                "validation_reason": f"Could not open image file: {str(e)}",
                "error": f"Image reading failed: {str(e)}"
            }
        
        # Validate MRI image BEFORE running prediction using STRICT validation from InferenceService
        inference_service = InferenceService(model_loader)
        is_valid, validation_confidence, validation_reason = inference_service.validate_brain_image(image)
        
        logger.info(f"MRI validation for {file.filename}: valid={is_valid}, confidence={validation_confidence}, reason={validation_reason}")
        
        # If image is not a valid MRI, return error response
        if not is_valid:
            return {
                "predictions": [],
                "top_prediction": None,
                "image_path": file_path,
                "model_version": None,
                "status": "invalid_image",
                "disclaimer": "⚠️ INVALID IMAGE: The uploaded file does not appear to be a valid brain MRI scan. Please upload a brain MRI image in JPEG, PNG, or DICOM format.",
                "is_valid_brain_image": False,
                "image_validation_confidence": validation_confidence,
                "validation_reason": validation_reason,
                "error": validation_reason
            }
        
        # Image is valid MRI - run model prediction
        prediction = await inference_service.predict_image(file_path)
        
        # Add disclaimer for successful predictions
        if prediction.get("is_valid_brain_image", False) and prediction.get("status") == "success":
            prediction["disclaimer"] = get_disclaimer()
        else:
            # For invalid images, provide a clear error message
            if prediction.get("status") == "invalid_image":
                prediction["disclaimer"] = "⚠️ INVALID IMAGE: The uploaded file is not a valid brain MRI scan. Please upload a brain MRI image in DICOM, JPEG, or PNG format."
        
        logger.info(f"Prediction completed for {file.filename}. Valid brain image: {prediction.get('is_valid_brain_image', False)}")
        
        return prediction
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
