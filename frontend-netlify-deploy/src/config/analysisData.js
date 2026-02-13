/**
 * Medical Analysis Data Configuration
 * Provides detailed, educational information for each tumor type
 * Based on medical literature and guidelines
 */

export const ANALYSIS_DATA = {
  "Glioma": {
    name: "Glioma",
    aboutResult: "The MRI analysis suggests possible glioma characteristics. Gliomas are tumors that originate from glial cells in the brain. They vary widely in grade and behavior. This analysis is for educational purposes only.",
    symptoms: [
      "Persistent headaches",
      "Vision or hearing changes",
      "Balance and coordination problems",
      "Nausea and vomiting",
      "Memory or concentration difficulties",
      "Personality or behavior changes"
    ],
    specialists: [
      "Neurologist - for diagnosis and neurological management",
      "Neurosurgeon - for surgical evaluation",
      "Neuro-oncologist - for tumor-specific treatment planning",
      "Radiologist - for imaging interpretation"
    ],
    lifestyle: [
      "Maintain a balanced, anti-inflammatory diet rich in fruits and vegetables",
      "Regular moderate exercise as tolerated",
      "Stress management through meditation or counseling",
      "Adequate sleep (7-8 hours nightly)",
      "Stay hydrated throughout the day",
      "Avoid smoking and limit alcohol"
    ],
    monitoring: [
      "Regular MRI follow-up imaging as recommended by specialists",
      "Clinical neurological evaluations",
      "Symptom monitoring and documentation",
      "Blood work monitoring as needed",
      "Specialist consultations per treatment plan"
    ],
    disclaimer: "This information is educational only. Only a qualified neurologist or neurosurgeon can provide diagnosis, prognosis, and treatment recommendations. Do not make medical decisions based solely on this analysis."
  },

  "Meningioma": {
    name: "Meningioma",
    aboutResult: "The MRI analysis suggests possible meningioma characteristics. Meningiomas are tumors that grow from the meninges (protective membranes surrounding the brain). Most are benign and slow-growing. This analysis is for educational purposes only.",
    symptoms: [
      "Headaches",
      "Vision problems",
      "Hearing changes or tinnitus",
      "Balance difficulties",
      "Cognitive changes or memory issues",
      "Seizures (in some cases)"
    ],
    specialists: [
      "Neurologist - for neurological assessment and symptom management",
      "Neurosurgeon - for surgical planning and intervention",
      "Radiologist - for detailed imaging analysis",
      "Neuro-oncologist - if additional treatment is needed"
    ],
    lifestyle: [
      "Maintain a healthy, balanced diet",
      "Regular mild to moderate exercise",
      "Stress reduction techniques",
      "Maintain consistent sleep schedule",
      "Stay well hydrated",
      "Avoid smoking and excessive alcohol"
    ],
    monitoring: [
      "Periodic MRI scans to monitor growth (if non-surgical management chosen)",
      "Neurological examinations",
      "Symptom tracking",
      "Specialist follow-up visits",
      "Watchful waiting approach when appropriate"
    ],
    disclaimer: "This information is educational only. Only a qualified medical professional can provide definitive diagnosis and treatment recommendations. Do not make medical decisions based solely on this analysis."
  },

  "Pituitary": {
    name: "Pituitary Tumor",
    aboutResult: "The MRI analysis suggests possible pituitary tumor characteristics. The pituitary gland controls many hormones in the body. Pituitary tumors vary in size and hormone-secreting activity. This analysis is for educational purposes only.",
    symptoms: [
      "Headaches",
      "Vision problems, especially peripheral vision loss",
      "Hormone imbalances leading to various symptoms",
      "Fatigue and weakness",
      "Weight changes",
      "Mood or personality changes"
    ],
    specialists: [
      "Endocrinologist - for hormone level evaluation and management",
      "Neurologist - for neurological symptoms",
      "Neurosurgeon - for surgical evaluation",
      "Ophthalmologist - for vision assessment"
    ],
    lifestyle: [
      "Maintain balanced nutrition with consistent meal timing",
      "Regular, gentle exercise appropriate to your energy levels",
      "Stress management and relaxation techniques",
      "Maintain regular sleep schedule",
      "Monitor hormone-related symptoms",
      "Stay hydrated"
    ],
    monitoring: [
      "Regular hormone level testing (blood work)",
      "Periodic MRI scans",
      "Vision assessments",
      "Neurological examinations",
      "Endocrinologist consultations",
      "Symptom documentation"
    ],
    disclaimer: "This information is educational only. Only a qualified endocrinologist and neurologist can diagnose and manage pituitary conditions. Hormone levels require professional monitoring. Do not modify hormone treatments without medical supervision."
  },

  "No Tumor": {
    name: "No Tumor Detected",
    aboutResult: "The MRI analysis did not detect characteristics consistent with a brain tumor. This is encouraging news. However, this analysis is for informational purposes and should be reviewed by a qualified radiologist or neurologist.",
    symptoms: [],
    specialists: [
      "Primary Care Physician - for overall health management",
      "Radiologist - to review the imaging",
      "Neurologist - if symptoms prompted this scan"
    ],
    lifestyle: [
      "Continue maintaining a healthy lifestyle",
      "Regular exercise and physical activity",
      "Balanced, nutritious diet",
      "Adequate sleep and stress management",
      "Regular health check-ups",
      "Avoid smoking and limit alcohol"
    ],
    monitoring: [
      "Follow up with your primary care physician",
      "If symptoms prompted this scan, discuss results with your doctor",
      "Continue routine health screening",
      "Report any new or concerning symptoms promptly"
    ],
    disclaimer: "This analysis is educational only. A qualified radiologist should formally interpret your MRI. If you have concerning symptoms, consult with your physician for proper evaluation."
  }
}

export default ANALYSIS_DATA
