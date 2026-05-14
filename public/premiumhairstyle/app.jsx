/* global React, ReactDOM, TopBar, Hero, Services, Works, Environment, Wash, Booking, LocationSection, Proof, Foot */

function App() {
  return (
    <>
      <TopBar />
      <Hero />
      <Services />
      <Works />
      <Environment />
      <Wash />
      <Booking />
      <LocationSection />
      <Proof />
      <Foot />
    </>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
