const API_BASE = '/api/v1'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options)

  if (!response.ok) {
    let message = 'Error en la solicitud'
    try {
      const data = await response.json()
      message = data.detail || message
    } catch {
      // ignore parse error
    }
    throw new Error(message)
  }

  return response
}

export async function register(payload) {
  const response = await request('/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  return response.json()
}

export async function login(payload) {
  const response = await request('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  return response.json()
}

export async function analyzeResume({ token, jobTitle, jobDescription, resumeFile }) {
  const formData = new FormData()
  formData.append('job_title', jobTitle)
  formData.append('job_description', jobDescription)
  formData.append('resume_file', resumeFile)

  const response = await request('/resume-analysis/analyze', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: formData,
  })

  return response.json()
}

export async function getHistory(token) {
  const response = await request('/resume-analysis/history', {
    headers: { Authorization: `Bearer ${token}` },
  })

  return response.json()
}

export function getExportPdfUrl(analysisId) {
  return `${API_BASE}/resume-analysis/${analysisId}/export-pdf`
}
