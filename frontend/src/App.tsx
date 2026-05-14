import { useEffect, useMemo, useState } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'ok' | 'error'>(
    'idle',
  )
  const [message, setMessage] = useState('')
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL as string | undefined

  const normalizedBaseUrl = useMemo(() => {
    if (!apiBaseUrl) return ''
    return apiBaseUrl.replace(/\/+$/, '')
  }, [apiBaseUrl])

  const checkHealth = async () => {
    if (!normalizedBaseUrl) {
      setStatus('error')
      setMessage('Missing VITE_API_BASE_URL in frontend .env file.')
      return
    }

    setStatus('loading')
    setMessage('')

    const controller = new AbortController()
    const timeoutId = window.setTimeout(() => controller.abort(), 8000)

    try {
      const response = await fetch(`${normalizedBaseUrl}/api/health`, {
        signal: controller.signal,
      })

      if (!response.ok) {
        setStatus('error')
        setMessage(`Backend returned ${response.status}`)
        return
      }

      const payload = (await response.json()) as { status?: string }
      setStatus('ok')
      setMessage(payload.status ?? 'Healthy')
    } catch (error) {
      setStatus('error')
      setMessage('Could not reach backend. Check CORS and API URL.')
    } finally {
      window.clearTimeout(timeoutId)
    }
  }

  useEffect(() => {
    void checkHealth()
  }, [normalizedBaseUrl])

  return (
    <div className="app">
      <header className="hero">
        <div className="badge">Inventory Platform</div>
        <h1>Frontend health monitor</h1>
        <p>
          React UI connects to the Django API using{' '}
          <code>VITE_API_BASE_URL</code>.
        </p>
      </header>

      <section className="grid">
        <article className="card">
          <h2>Backend status</h2>
          <p className={`status ${status}`}>
            {status === 'loading' && 'Checking...'}
            {status === 'ok' && `Healthy: ${message}`}
            {status === 'error' && message}
            {status === 'idle' && 'Waiting for check'}
          </p>
          <button type="button" className="primary" onClick={checkHealth}>
            Recheck /api/health
          </button>
        </article>

        <article className="card">
          <h2>Connection info</h2>
          <dl>
            <div>
              <dt>API base URL</dt>
              <dd>{normalizedBaseUrl || 'Not set'}</dd>
            </div>
            <div>
              <dt>Expected endpoint</dt>
              <dd>/api/health</dd>
            </div>
            <div>
              <dt>Required env key</dt>
              <dd>VITE_API_BASE_URL</dd>
            </div>
          </dl>
        </article>
      </section>

      <section className="card tips">
        <h2>Frontend checklist</h2>
        <ul>
          <li>No console errors when loading the page.</li>
          <li>API URL is always read from environment variables.</li>
          <li>Health endpoint responds with status code 200.</li>
          <li>UI works on mobile and desktop.</li>
        </ul>
      </section>
    </div>
  )
}

export default App
