// script_carrossel.js (NEOLIBRES)

document.addEventListener("DOMContentLoaded", () => {
  const slidesContainer = document.querySelector(".slides");
  if (!slidesContainer) {
    // Se o contêiner de slides não for encontrado, significa que não há carrossel nesta página,
    // então a função pode sair sem causar erros.
    return;
  }

  const slides = document.querySelectorAll(".slide");
  const totalSlides = slides.length;
  let currentIndex = 0;

  function updateSlidePosition() {
    // Calcula a posição do transform CSS para mover os slides
    slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
  }

  // Apenas inicia o carrossel se houver slides
  if (totalSlides > 0) {
    function nextSlide() {
      // Avança para o próximo slide, voltando ao primeiro se chegar ao final
      currentIndex = (currentIndex + 1) % totalSlides;
      updateSlidePosition();
    }
    
    // Define um intervalo para trocar os slides automaticamente
    // O tempo de 5000ms (5 segundos) é um bom padrão para carrosséis
    setInterval(nextSlide, 4000); 
  }
});