/* global React */

const HOURS = [
  { d: 'Monday',    h: '10:00 – 18:00' },
  { d: 'Tuesday',   h: '10:00 – 18:00' },
  { d: 'Wednesday', h: '10:00 – 18:00' },
  { d: 'Thursday',  h: '10:00 – 18:00' },
  { d: 'Friday',    h: '10:00 – 18:00' },
  { d: 'Saturday',  h: '10:00 – 18:00' },
  { d: 'Sunday',    h: '10:00 – 18:00' },
];

function Booking() {
  const todayIdx = (new Date().getDay() + 6) % 7; // Mon=0
  return (
    <section className="book-section" id="book">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">06 · Booking</span>
          <h2>Book online.<br/>Or just walk in.</h2>
          <p>Booking is handled through Fresha — you'll see live availability and can pick a stylist. Walk-ins are always welcome too.</p>
        </div>

        <div className="book-grid">
          <div className="book-card">
            <h3 className="book-title">Reserve your chair</h3>
            <p className="book-sub">Pick a date, time and stylist. You'll get a text reminder the day before — no deposits, no fuss.</p>
            <div className="book-cta-row">
              <a className="cta cta-glow cta-lg" href={window.BUSINESS.freshaUrl} target="_blank" rel="noopener noreferrer">
                Open Fresha
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M5 3l4 4-4 4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </a>
              <a className="cta cta-light cta-lg" href="#services">
                See services
              </a>
            </div>
            <div className="book-walkin">
              <span className="walkin-dot" />
              <div>
                <div style={{ color: '#fff', fontWeight: 600 }}>Walk-ins welcome today</div>
                <div style={{ fontSize: 12.5, opacity: 0.7, marginTop: 3 }}>Typical wait: 15–30 min · 4 stylists rostered</div>
              </div>
            </div>
            <div className="fresha-mark">
              <svg width="10" height="10" viewBox="0 0 10 10" fill="currentColor"><circle cx="5" cy="5" r="2"/></svg>
              Powered by Fresha
            </div>
          </div>

          <div className="hours-card">
            <h3>Opening hours</h3>
            <div className="sub zh">营业时间 · 全周 7 天</div>
            {HOURS.map((h, i) => (
              <div key={h.d} className={`hour-row ${i === todayIdx ? 'today' : ''}`}>
                <span className="d">
                  {h.d}
                  {i === todayIdx && <span className="today-pill">TODAY</span>}
                </span>
                <span className="h">{h.h}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function MapMini() {
  return (
    <svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid slice" style={{ width: '100%', height: '100%', display: 'block' }}>
      <defs>
        <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="0.6" fill="#C8C0B0" />
        </pattern>
      </defs>
      <rect width="600" height="400" fill="#ECE5DA"/>
      <rect width="600" height="400" fill="url(#dots)"/>
      {/* Burwood Hwy horizontal */}
      <rect x="0" y="180" width="600" height="44" fill="#FAF6F0" stroke="#D9D2C7"/>
      <line x1="0" y1="202" x2="600" y2="202" stroke="#E8B774" strokeWidth="1.5" strokeDasharray="8 8" opacity="0.5"/>
      {/* Middleborough Rd vertical */}
      <rect x="260" y="0" width="34" height="400" fill="#FAF6F0" stroke="#D9D2C7"/>
      {/* Side street */}
      <rect x="0" y="320" width="600" height="14" fill="#FAF6F0" stroke="#D9D2C7"/>
      {/* Labels */}
      <text x="30" y="172" fontFamily="JetBrains Mono, monospace" fontSize="10" fill="#79706A" letterSpacing="0.12em">BURWOOD HWY</text>
      <text x="304" y="40" fontFamily="JetBrains Mono, monospace" fontSize="10" fill="#79706A" letterSpacing="0.12em">MIDDLEBOROUGH RD</text>
      {/* Buildings: Burwood One block */}
      <rect x="40" y="240" width="200" height="70" fill="#D9D4CC" rx="3"/>
      <text x="58" y="282" fontFamily="Plus Jakarta Sans" fontSize="13" fill="#3A332C" fontWeight="700">BURWOOD ONE</text>
      <text x="58" y="298" fontFamily="Plus Jakarta Sans" fontSize="10" fill="#79706A">Shopping Centre</text>
      {/* Other buildings */}
      <rect x="320" y="240" width="90" height="40" fill="#E6DFD3" rx="3"/>
      <rect x="430" y="240" width="140" height="70" fill="#E6DFD3" rx="3"/>
      <rect x="80" y="80" width="120" height="80" fill="#E6DFD3" rx="3"/>
      <rect x="320" y="80" width="90" height="50" fill="#E6DFD3" rx="3"/>
      <rect x="430" y="80" width="140" height="80" fill="#E6DFD3" rx="3"/>
      <rect x="320" y="350" width="120" height="40" fill="#E6DFD3" rx="3"/>
      {/* Pin */}
      <g transform="translate(140, 268)">
        <circle r="22" fill="#171513" opacity="0.08"/>
        <circle r="14" fill="#171513"/>
        <circle r="5" fill="#E8B774"/>
      </g>
      <g transform="translate(140, 232)">
        <rect x="-50" y="-22" width="100" height="22" rx="4" fill="#171513"/>
        <text x="0" y="-7" textAnchor="middle" fontFamily="Plus Jakarta Sans" fontSize="11" fill="#FAF6F0" fontWeight="700" letterSpacing="0.04em">PREMIUM</text>
      </g>
      {/* Compass */}
      <g transform="translate(548, 40)">
        <circle r="18" fill="rgba(250,246,240,0.85)" stroke="#D9D2C7"/>
        <path d="M0 -10 L4 8 L0 4 L-4 8 Z" fill="#171513"/>
        <text x="0" y="-12" textAnchor="middle" fontFamily="JetBrains Mono" fontSize="8" fill="#79706A">N</text>
      </g>
    </svg>
  );
}

function LocationSection() {
  return (
    <section id="location">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">07 · Find Us</span>
          <h2>Burwood One.<br/>Ground floor.</h2>
          <p>Inside Burwood One Shopping Centre. Look for the timber storefront and the bright PREMIUM sign.</p>
        </div>
        <div className="loc-grid">
          <div className="loc-map">
            <MapMini />
          </div>
          <div className="loc-body">
            <div className="loc-eyebrow">Address</div>
            <div className="loc-name">{window.BUSINESS.name}</div>
            <div className="loc-addr">
              Shop G42<br/>
              172–210 Burwood Hwy<br/>
              Burwood East VIC 3151
            </div>
            <div className="loc-meta">
              <div className="loc-meta-row">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <circle cx="7" cy="7" r="5.8" stroke="currentColor" strokeWidth="1.2"/>
                  <path d="M7 4v3l2 1.4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
                </svg>
                Open today · 10:00 – 18:00
              </div>
              <div className="loc-meta-row">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <rect x="1.5" y="2.5" width="11" height="9" rx="1.5" stroke="currentColor" strokeWidth="1.2"/>
                  <path d="M1.5 5h11" stroke="currentColor" strokeWidth="1.2"/>
                </svg>
                Free 3-hour parking in shopping centre
              </div>
              <div className="loc-meta-row">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M3 11l4-8 4 8" stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round"/>
                  <path d="M4.5 8.5h5" stroke="currentColor" strokeWidth="1.2"/>
                </svg>
                Near Coles entrance · ground floor
              </div>
            </div>
            <div className="loc-actions">
              <a className="cta cta-primary" href={window.BUSINESS.mapsUrl} target="_blank" rel="noopener noreferrer">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M7 1l1.5 4.5L13 7l-4.5 1.5L7 13 5.5 8.5 1 7l4.5-1.5L7 1z" fill="currentColor"/>
                </svg>
                Get directions
              </a>
              <a className="cta cta-ghost" href={window.BUSINESS.freshaUrl} target="_blank" rel="noopener noreferrer">
                Book a chair
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Proof() {
  return (
    <section className="proof-section" id="reviews">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">08 · Trusted Locally</span>
          <h2>Trusted by students<br/>&amp; families.</h2>
          <p>Affordable modern cuts for everyday life — that's what our regulars come back for.</p>
        </div>

        <div className="stat-row">
          <div className="stat">
            <div className="stat-num">4.8<span className="unit">/5</span></div>
            <div className="stat-lbl">Google rating</div>
          </div>
          <div className="stat">
            <div className="stat-num">320<span className="unit">+</span></div>
            <div className="stat-lbl">Customer reviews</div>
          </div>
          <div className="stat">
            <div className="stat-num">7<span className="unit">yrs</span></div>
            <div className="stat-lbl">Serving Burwood</div>
          </div>
        </div>

        <div className="reviews-grid">
          <div className="review">
            <div className="review-stars">★★★★★</div>
            <div className="review-body">
              "Honest pricing and they actually listen. Got a fringe trim and ladies cut, $45 total, no surprise fees. Will be back."
            </div>
            <div className="review-foot">
              <div className="review-avatar">L</div>
              <div>
                <div className="review-name">Linda C.</div>
                <div className="review-meta">Local guide · 2 weeks ago</div>
              </div>
            </div>
          </div>
          <div className="review">
            <div className="review-stars">★★★★★</div>
            <div className="review-body">
              "离学校近，价格也合理。Skin fade $35 还包洗发，比 CBD 便宜一半。师傅手艺很稳，每次都剪得很满意。"
            </div>
            <div className="review-foot">
              <div className="review-avatar" style={{ background: 'var(--ink)' }}>K</div>
              <div>
                <div className="review-name">Kevin Z.</div>
                <div className="review-meta"><span className="zh">学生</span> · 1 month ago</div>
              </div>
            </div>
          </div>
          <div className="review">
            <div className="review-stars">★★★★★</div>
            <div className="review-body">
              "Took my 4-year-old here, the toy car seat kept him calm the whole time. Cut was sharp, friendly staff. Found our family salon."
            </div>
            <div className="review-foot">
              <div className="review-avatar" style={{ background: 'var(--accent)' }}>M</div>
              <div>
                <div className="review-name">Mia R.</div>
                <div className="review-meta">3 weeks ago</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Foot() {
  return (
    <footer className="foot">
      <div className="container">
        <div className="foot-grid">
          <div>
            <div className="foot-brand-name">Premium Hairstyles &<br/>Premium Quick Cuts</div>
            <div className="foot-zh zh">高质量发型 · 快剪服务</div>
            <div className="foot-blurb">A modern Burwood salon for everyday cuts. Honest pricing, no upsell, walk-ins welcome.</div>
          </div>
          <div className="foot-col">
            <h4>Visit</h4>
            <div className="foot-links">
              <a href={window.BUSINESS.mapsUrl} target="_blank" rel="noopener noreferrer">Shop G42, 172–210 Burwood Hwy</a>
              <a href={window.BUSINESS.mapsUrl} target="_blank" rel="noopener noreferrer">Burwood East VIC 3151</a>
              <a href={window.BUSINESS.mapsUrl} target="_blank" rel="noopener noreferrer">Get directions →</a>
            </div>
          </div>
          <div className="foot-col">
            <h4>Hours</h4>
            <div className="foot-links">
              <a>Mon – Sun</a>
              <a>10:00 – 18:00</a>
              <a>Open 7 days</a>
            </div>
          </div>
          <div className="foot-col">
            <h4>Site</h4>
            <div className="foot-links">
              <a href="#services">Services &amp; pricing</a>
              <a href="#salon">Salon photos</a>
              <a href={window.BUSINESS.freshaUrl} target="_blank" rel="noopener noreferrer">Book on Fresha</a>
              <a href="#reviews">Reviews</a>
            </div>
          </div>
        </div>
        <div className="foot-bottom">
          <div>© 2026 Premium Hairstyles · Burwood One</div>
          <div>Booking powered by Fresha</div>
        </div>
      </div>
    </footer>
  );
}

window.Booking = Booking;
window.LocationSection = LocationSection;
window.Proof = Proof;
window.Foot = Foot;
