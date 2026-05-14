/* global React */

const BUSINESS = {
  name: 'Premium Hairstyles & Premium Quick Cuts',
  shortName: 'PREMIUM',
  tagline: 'Hair Style · Quick Cuts',
  address1: 'Shop G42, 172–210 Burwood Hwy',
  address2: 'Burwood East VIC 3151',
  hours: '10:00 – 18:00, open 7 days',
  freshaUrl: 'https://www.fresha.com/a/premium-hairstyles-premium-quick-cuts-burwood-east-burwood-one-shopping-centre-shop-g42-172-210-burwood-highway-au1lqv4f',
  mapsUrl: 'https://maps.app.goo.gl/ko4AzxXYJXyifuXW7',
};

function BrandMark() {
  return (
    <a href="#top" className="brand-lockup" style={{ textDecoration: 'none', color: 'inherit' }}>
      <div className="brand-mark">P</div>
      <div className="brand-text">
        <div className="brand-name">PREMIUM</div>
        <div className="brand-sub">Hair Style · Quick Cuts</div>
      </div>
    </a>
  );
}

function TopBar() {
  return (
    <header className="topbar">
      <div className="container topbar-inner">
        <BrandMark />
        <nav className="nav-links">
          <a href="#services">Services</a>
          <a href="#work">Recent work</a>
          <a href="#salon">Salon</a>
          <a href="#location">Find us</a>
        </nav>
        <div className="nav-right">
          <span className="lang-pill">
            <span>EN</span>
            <span style={{ opacity: 0.4 }}>/</span>
            <span className="zh">中文</span>
          </span>
          <a className="cta cta-primary" href={BUSINESS.freshaUrl} target="_blank" rel="noopener noreferrer">
            Book on Fresha
          </a>
        </div>
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section className="hero" id="top">
      <img src="images/storefront.avif" alt="Premium Hairstyles storefront at Burwood One" />
      <div className="container hero-inner">
        <div className="hero-status">
          <span className="status-dot" />
          Open today · 10:00 – 18:00
        </div>
        <div className="hero-body">
          <div className="hero-zh">高质量 · 实惠价格 · 欢迎到店</div>
          <h1 className="hero-title">
            Quality cuts.<br />
            <em>Honest</em> prices.
          </h1>
          <p className="hero-sub">A modern Burwood salon for everyday cuts — practical, clean, and friendly. No upsell, no surprises.</p>
          <div className="hero-tags">
            <span className="hero-tag">Walk-ins welcome</span>
            <span className="hero-tag">Open 7 days</span>
            <span className="hero-tag">Burwood One</span>
            <span className="hero-tag">中文 OK</span>
          </div>
          <div className="hero-cta-row">
            <a className="cta cta-glow cta-lg" href={BUSINESS.freshaUrl} target="_blank" rel="noopener noreferrer">
              Book on Fresha
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M3 7h8m-3-3l3 3-3 3" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </a>
            <a className="cta cta-light cta-lg" href="#location">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M7 13s5-4.5 5-8a5 5 0 10-10 0c0 3.5 5 8 5 8z" stroke="currentColor" strokeWidth="1.4"/>
                <circle cx="7" cy="5" r="1.6" stroke="currentColor" strokeWidth="1.4"/>
              </svg>
              Find us
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

window.BUSINESS = BUSINESS;
window.BrandMark = BrandMark;
window.TopBar = TopBar;
window.Hero = Hero;
