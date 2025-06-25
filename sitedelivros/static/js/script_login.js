particlesJS("particles-js", {
  particles: {
    number: {
      value: 60,
      density: { enable: true, value_area: 800 }
    },
    color: {
      value: "#ef4444"  // vermelho coral da NeoLibris
    },
    shape: {
      type: "circle",
      stroke: { width: 0, color: "#000000" }
    },
    opacity: {
      value: 0.6,
      random: false
    },
    size: {
      value: 3,
      random: true
    },
    line_linked: {
      enable: true,
      distance: 150,
      color: "#ef4444",
      opacity: 0.5,
      width: 1
    },
    move: {
      enable: true,
      speed: 3,
      direction: "none",
      out_mode: "out"
    }
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: { enable: true, mode: "grab" },  // interage com o mouse
      onclick: { enable: false },
      resize: true
    },
    modes: {
      grab: {
        distance: 200,
        line_linked: { opacity: 0.7 }
      }
    }
  },
  retina_detect: true
});
