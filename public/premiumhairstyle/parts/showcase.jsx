/* global React */

function Works() {
  return (
    <section id="work">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">03 · Recent Work</span>
          <h2>Cuts &amp; colour.</h2>
          <p>Real customers, real results — straight from the chair, nothing retouched.</p>
        </div>
        <div className="work-grid">
          <div className="work-card"><img src="images/work-blonde.png" alt="Blonde balayage"/><span className="tag">Balayage</span></div>
          <div className="work-card"><img src="images/work-burgundy.png" alt="Burgundy"/><span className="tag">Colour</span></div>
          <div className="work-card"><img src="images/work-grey-long.png" alt="Ash grey long"/><span className="tag">Ash grey</span></div>
          <div className="work-card"><img src="images/work-star-fade.png" alt="Star fade kids"/><span className="tag">Kids fade</span></div>
        </div>
      </div>
    </section>
  );
}

function Environment() {
  return (
    <section className="env-section" id="salon">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">04 · The Salon</span>
          <h2>Warm timber.<br/>Soft concrete.</h2>
          <p>A practical, modern space built for everyday cuts — clean lighting, comfortable chairs, separate wash room.</p>
        </div>
        <div className="env-grid">
          <div className="env-tile t-a">
            <img src="images/interior-wood.avif" alt="Salon timber styling stations" />
            <div className="cap">
              <span>Styling stations</span>
              <span className="pin">01 / 05</span>
            </div>
          </div>
          <div className="env-tile t-b">
            <img src="images/stylist-ladies.png" alt="Stylist working" style={{ objectPosition: 'center top' }} />
            <div className="cap"><span>In session</span><span className="pin">02 / 05</span></div>
          </div>
          <div className="env-tile t-c">
            <img src="images/interior-concrete.avif" alt="Concrete column area" />
            <div className="cap"><span>Main floor</span><span className="pin">03 / 05</span></div>
          </div>
          <div className="env-tile t-d">
            <img src="images/storefront.avif" alt="Storefront" />
            <div className="cap"><span>Front of house</span><span className="pin">04 / 05</span></div>
          </div>
          <div className="env-tile t-e">
            <img src="images/kids-apron.png" alt="Kids cut in progress" />
            <div className="cap"><span>Kids cuts</span><span className="pin">05 / 05</span></div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Wash() {
  return (
    <section className="wash-section" id="wash">
      <div className="container">
        <div className="wash-grid">
          <div className="wash-img">
            <img src="images/wash-station.jpg" alt="Reclined wash station" />
          </div>
          <div>
            <span className="eyebrow wash-eyebrow">05 · Wash & Care</span>
            <h2 className="wash-title">Reclined wash.<br/>Quiet room.</h2>
            <div className="wash-zh zh">舒缓洗发 · 头部按摩</div>
            <p className="wash-lead">Heated chairs, NATULIQUE organic shampoo, and a separate wash room — no rushed sink at the styling chair.</p>
            <ul className="wash-list">
              <li><span className="n">01</span><span>Heated reclining chair</span><span className="zh-side zh">恒温躺椅</span></li>
              <li><span className="n">02</span><span>NATULIQUE organic shampoo</span><span className="zh-side zh">有机洗发</span></li>
              <li><span className="n">03</span><span>3-minute scalp massage</span><span className="zh-side zh">头部按摩</span></li>
              <li><span className="n">04</span><span>Warm towel finish</span><span className="zh-side zh">热毛巾收尾</span></li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

window.Works = Works;
window.Environment = Environment;
window.Wash = Wash;
