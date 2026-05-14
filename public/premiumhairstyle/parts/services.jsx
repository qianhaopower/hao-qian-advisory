/* global React */

const SERVICES = [
  { id: 1, name: "Men's Cut",   zh: '男士剪发',   desc: 'Wash, cut and finish. 30 min.',                       price: 25, tag: 'Most popular' },
  { id: 2, name: "Ladies' Cut", zh: '女士剪发',   desc: 'Wash, cut and blow-dry. 45 min.',                     price: 35, tag: 'Signature', feat: true },
  { id: 3, name: 'Skin Fade',   zh: '渐变剃刀',   desc: 'Clipper fade with sharp line-up. 35 min.',            price: 35, tag: 'Barber' },
  { id: 4, name: 'Under Cut',   zh: '内推剪',     desc: 'Top length cut with clipper sides. 30 min.',          price: 30, tag: 'Trending' },
  { id: 5, name: 'Kids Cut',    zh: '儿童剪发',   desc: 'Under 12 · car seat & lollipop on the house. 25 min.', price: 20, tag: 'Family' },
  { id: 6, name: 'Fringe Trim', zh: '修刘海',     desc: 'Quick maintenance between cuts. 10 min.',             price: 10, tag: 'Walk-in' },
];

function Services() {
  return (
    <section id="services">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">02 · Services & Pricing</span>
          <h2>Simple menu.<br/>No upsell.</h2>
          <p>Walk-in or book ahead — same price either way. All prices in AUD. Colouring, perming, treatments and head-spa are quoted in-salon after a quick consultation.</p>
        </div>

        <div className="services-grid">
          {SERVICES.map((s, i) => (
            <a
              key={s.id}
              className={`service-card ${s.feat ? 'feat' : ''}`}
              href={window.BUSINESS.freshaUrl}
              target="_blank" rel="noopener noreferrer"
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <div className="service-num">{String(i + 1).padStart(2, '0')} / {String(SERVICES.length).padStart(2, '0')}</div>
              <div className="service-name">{s.name}</div>
              <div className="service-zh zh">{s.zh}</div>
              <div className="service-desc">{s.desc}</div>
              <div className="service-foot">
                <div className="service-price"><span className="cur">$</span>{s.price}</div>
                <div className="service-tag">{s.tag}</div>
              </div>
            </a>
          ))}

          <div className="services-note">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <circle cx="9" cy="9" r="7.5" stroke="currentColor" strokeWidth="1.3"/>
              <path d="M9 5v4.5M9 12v.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            <div>
              Colouring &amp; treatments quoted in-salon. <span className="zh" style={{ color: 'var(--muted)' }}>染发／烫发／护理到店咨询，价格透明，绝不强推。</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

window.Services = Services;
