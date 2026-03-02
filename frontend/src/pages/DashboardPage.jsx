import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { analyzeResume, getHistory } from '../api/client'
import { useAuth } from '../context/AuthContext'

export default function DashboardPage() {
  const { token } = useAuth()
  const navigate = useNavigate()
  const [jobTitle, setJobTitle] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [resumeFile, setResumeFile] = useState(null)
  const [history, setHistory] = useState([])
  const [error, setError] = useState('')
  const [loadingSubmit, setLoadingSubmit] = useState(false)
  const [loadingHistory, setLoadingHistory] = useState(true)

  const loadHistory = async () => {
    setLoadingHistory(true)
    try {
      const data = await getHistory(token)
      setHistory(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoadingHistory(false)
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')

    if (!resumeFile) {
      setError('Seleccioná un archivo de CV antes de continuar.')
      return
    }

    setLoadingSubmit(true)
    try {
      const data = await analyzeResume({ token, jobTitle, jobDescription, resumeFile })
      setJobTitle('')
      setJobDescription('')
      setResumeFile(null)
      await loadHistory()
      navigate(`/resultados/${data.analysis_id}`, { state: { result: data } })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoadingSubmit(false)
    }
  }

  return (
    <div className="grid">
      <section className="card">
        <h2>Subir CV y analizar</h2>
        <form onSubmit={handleSubmit} className="form">
          <label>
            Puesto al que aplicás
            <input value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} required />
          </label>

          <label>
            Descripción del puesto
            <textarea
              rows={7}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              required
            />
          </label>

          <label>
            Archivo de CV (.txt o .pdf)
            <input
              type="file"
              accept=".txt,.pdf"
              onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
              required
            />
          </label>

          {error && <p className="error">{error}</p>}

          <button className="btn-primary" type="submit" disabled={loadingSubmit}>
            {loadingSubmit ? 'Analizando...' : 'Subir CV y analizar'}
          </button>
        </form>
      </section>

      <section className="card">
        <h2>Resultados recientes</h2>
        {loadingHistory ? (
          <p>Cargando historial...</p>
        ) : history.length === 0 ? (
          <p>Todavía no hay análisis guardados.</p>
        ) : (
          <ul className="history-list">
            {history.map((item) => (
              <li key={item.id}>
                <div>
                  <strong>{item.job_title}</strong>
                  <p>{item.resume_filename}</p>
                  <small>Score: {item.score}%</small>
                </div>
                <Link to={`/resultados/${item.id}`}>Ver resultado</Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}
