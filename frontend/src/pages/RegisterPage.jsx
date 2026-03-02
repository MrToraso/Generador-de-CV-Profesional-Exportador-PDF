import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../api/client'

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', full_name: '', password: '' })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const update = (field) => (event) => {
    setForm((prev) => ({ ...prev, [field]: event.target.value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      await register(form)
      setSuccess('Cuenta creada correctamente. Ahora podés iniciar sesión.')
      setTimeout(() => navigate('/login'), 1000)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card auth-card">
      <h1>Crear cuenta</h1>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Nombre completo
          <input value={form.full_name} onChange={update('full_name')} minLength={2} required />
        </label>

        <label>
          Email
          <input type="email" value={form.email} onChange={update('email')} required />
        </label>

        <label>
          Contraseña
          <input
            type="password"
            value={form.password}
            onChange={update('password')}
            minLength={8}
            required
          />
        </label>

        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}

        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? 'Creando cuenta...' : 'Registrarme'}
        </button>
      </form>
      <p>
        ¿Ya tenés cuenta? <Link to="/login">Iniciá sesión</Link>
      </p>
    </section>
  )
}
