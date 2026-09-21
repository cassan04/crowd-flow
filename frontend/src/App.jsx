import { useEffect, useState } from 'react'
import { CircleMarker, MapContainer, TileLayer, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import './App.css'

const defaultCenter = [40.4168, -3.7038]

const nearbyPlaces = [
  { name: 'Museo del Prado', type: 'Museo', occupancy: '84/300 personas', percentage: 28, state: 'Poco concurrido', tone: 'quiet' },
  { name: 'Mega Gym Center', type: 'Gimnasio', occupancy: '192/300 personas', percentage: 64, state: 'Moderado', tone: 'medium' },
  { name: 'C.C. El Corte Inglés', type: 'Centro Comercial', occupancy: '1240/1400 personas', percentage: 88, state: 'Muy concurrido', tone: 'busy' },
]

function RecenterMap({ position }) {
  const map = useMap()

  useEffect(() => {
    if (position) map.flyTo(position, 15, { duration: 1.2 })
  }, [map, position])

  return null
}

function App() {
  const [position, setPosition] = useState(null)
  const [locationStatus, setLocationStatus] = useState(() => (
    navigator.geolocation ? 'loading' : 'unsupported'
  ))

  useEffect(() => {
    if (!navigator.geolocation) return

    navigator.geolocation.getCurrentPosition(
      ({ coords }) => {
        setPosition([coords.latitude, coords.longitude])
        setLocationStatus('ready')
      },
      () => setLocationStatus('denied'),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 },
    )
  }, [])

  const requestLocation = () => {
    setLocationStatus('loading')
    navigator.geolocation?.getCurrentPosition(
      ({ coords }) => {
        setPosition([coords.latitude, coords.longitude])
        setLocationStatus('ready')
      },
      () => setLocationStatus('denied'),
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 },
    )
  }

  return (
    <main className="app-shell">
      <section className="map-stage" aria-label="Mapa de lugares cercanos">
        <MapContainer center={defaultCenter} zoom={13} zoomControl={false} className="map">
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <RecenterMap position={position} />
          {position && <CircleMarker center={position} radius={9} pathOptions={{ color: '#ffffff', weight: 4, fillColor: '#0a9f83', fillOpacity: 1 }} />}
        </MapContainer>

        <header className="top-bar">
          <span className="wordmark">crowd<span>flow</span></span>
          <button type="button" className="profile-button" aria-label="Abrir perfil">MP</button>
        </header>

        <div className="map-tools">
          <label className="search-box">
            <span aria-hidden="true">⌕</span>
            <input type="search" placeholder="Buscar museos, gimnasios, tiendas..." aria-label="Buscar lugares" />
            <span className="voice-icon" aria-hidden="true">◉</span>
          </label>
          <div className="category-list" aria-label="Categorías de lugares">
            <button type="button" className="category active">Museos</button>
            <button type="button" className="category">Comerciales</button>
            <button type="button" className="category">Gimnasios</button>
            <button type="button" className="category">Salas</button>
          </div>
        </div>

        <button type="button" className="locate-button" onClick={requestLocation} aria-label="Centrar en mi ubicación">⊙</button>
        <div className="map-pin pin-green" aria-hidden="true">♜</div>
        <div className="map-pin pin-red" aria-hidden="true">▣</div>
        <div className="map-pin pin-orange" aria-hidden="true">⌁</div>

        {locationStatus === 'denied' && (
          <div className="location-notice" role="status">
            <strong>Activa tu ubicación</strong>
            <span>Necesitamos permiso para mostrarte lugares cercanos.</span>
            <button type="button" onClick={requestLocation}>Intentar de nuevo</button>
          </div>
        )}
      </section>

      <section className="places-panel" aria-labelledby="nearby-title">
        <div className="panel-handle" aria-hidden="true" />
        <div className="panel-heading">
          <h1 id="nearby-title">Lugares populares cercanos</h1>
          <button type="button">Ver todos</button>
        </div>
        <div className="place-list">
          {nearbyPlaces.map((place) => (
            <article className="place-card" key={place.name}>
              <div className="place-copy">
                <h2>{place.name}</h2>
                <p>{place.type} · {place.occupancy}</p>
                <div className="capacity-line"><span style={{ width: `${place.percentage}%` }} /></div>
                <small>Aforo: <b>{place.percentage}%</b></small>
              </div>
              <span className={`status-pill ${place.tone}`}><i />{place.state}</span>
            </article>
          ))}
        </div>
      </section>

      <nav className="bottom-nav" aria-label="Navegación principal">
        <button type="button" className="nav-item selected"><span aria-hidden="true">⌖</span>Mapa</button>
        <button type="button" className="nav-item"><span aria-hidden="true">◉</span>Buscar</button>
        <button type="button" className="nav-item"><span aria-hidden="true">♙</span>Mis lugares</button>
      </nav>
    </main>
  )
}

export default App
