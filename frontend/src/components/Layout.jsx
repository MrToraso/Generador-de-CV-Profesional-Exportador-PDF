import { Link, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Layout() {
  const { isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <Link to={isAuthenticated ? '/dashboard' : '/login'} className="brand">
          ResumeFix
        </Link>
        <nav>
          {isAuthenticated ? (
            <button onClick={handleLogout} className="btn-secondary">
              Cerrar sesión
            </button>
          ) : (
            <div className="auth-links">
              <Link to="/login">Login</Link>
              <Link to="/registro">Registro</Link>
            </div>
          )}
        </nav>
      </header>
      <main className="container">
        <Outlet />
      </main>
    </div>
  )
}
