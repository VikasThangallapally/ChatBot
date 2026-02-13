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


def get_absolute_image_url(file_path: str) -> str:
    """
    Convert local file path to absolute URL with full backend domain.
    Example: app/static/uploads/image.jpg -> https://backend.onrender.com/static/uploads/image.jpg
    """
    # Extract relative path from uploads directory
    if settings.UPLOAD_DIR in file_path:
        relative_path = file_path.replace(settings.UPLOAD_DIR, "").lstrip("/\\")
    else:
        relative_path = os.path.basename(file_path)
    
    # Construct absolute URL with BACKEND_URL
    absolute_url = f"{settings.BACKEND_URL.rstrip('/')}/static/{relative_path}"
    return absolute_url


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
        
        # Get absolute URL for the image
        image_url = get_absolute_image_url(file_path)
        
        # Initialize inference service (which includes validation)
        inference_service = InferenceService(model_loader)
        
        # Run inference - this includes validation internally
        prediction = await inference_service.predict_image(file_path)
        
        # Replace local file path with absolute URL
        prediction["image_path"] = image_url
        
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
