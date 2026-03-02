import { useEffect, useState } from 'react'
import { useLocation, useParams } from 'react-router-dom'
import { getExportPdfUrl, getHistory } from '../api/client'
import { useAuth } from '../context/AuthContext'

export default function ResultPage() {
  const { analysisId } = useParams()
  const location = useLocation()
  const { token } = useAuth()
  const [result, setResult] = useState(location.state?.result || null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (result) return

    const loadFromHistory = async () => {
      try {
        const history = await getHistory(token)
        const match = history.find((item) => String(item.id) === analysisId)
        if (!match) {
          setError('No se encontró ese análisis en el historial.')
          return
        }

        setResult({
          analysis_id: match.id,
          score: match.score,
          matched_keywords: [],
          missing_keywords: [],
          matched_keywords_count: 0,
          total_keywords_count: 0,
          created_at: match.created_at,
        })
      } catch (err) {
        setError(err.message)
      }
    }

    loadFromHistory()
  }, [analysisId, result, token])

  const downloadPdf = async () => {
    try {
      const response = await fetch(getExportPdfUrl(analysisId), {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (!response.ok) {
        throw new Error('No se pudo generar el PDF.')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const anchor = document.createElement('a')
      anchor.href = url
      anchor.download = `resumefix_optimized_${analysisId}.pdf`
      anchor.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      setError(err.message)
    }
  }

  if (error) {
    return <p className="error">{error}</p>
  }

  if (!result) {
    return <p>Cargando resultado...</p>
  }

  return (
    <section className="card">
      <h1>Resultado del análisis #{result.analysis_id}</h1>
      <p className="score">Score de compatibilidad: {result.score}%</p>

      <div className="keywords-grid">
        <div>
          <h3>Palabras clave encontradas</h3>
          {result.matched_keywords.length === 0 ? (
            <p>No disponibles para este análisis.</p>
          ) : (
            <ul>
              {result.matched_keywords.map((keyword) => (
                <li key={keyword}>{keyword}</li>
              ))}
            </ul>
          )}
        </div>

        <div>
          <h3>Palabras clave faltantes</h3>
          {result.missing_keywords.length === 0 ? (
            <p>No disponibles para este análisis.</p>
          ) : (
            <ul>
              {result.missing_keywords.map((keyword) => (
                <li key={keyword}>{keyword}</li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <button className="btn-primary" onClick={downloadPdf}>
        Generar PDF optimizado
      </button>
    </section>
  )
}
