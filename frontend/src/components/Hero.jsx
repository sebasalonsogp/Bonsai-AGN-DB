import { useRef, useEffect } from "react";

export default function Hero() {
    const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const starsRef = useRef([]);  // Store stars in a ref to avoid initialization issues

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Generate initial stars
    function generateStars() {
      const stars = [];
      
      // Small stars
      for (let i = 0; i < 150; i++) {
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 1.5,
          baseOpacity: Math.random() * 0.7 + 0.3,
          opacity: Math.random() * 0.7 + 0.3,
          speed: Math.random() * 0.00001 + 0.0001,
          twinkleDirection: Math.random() > 0.5 ? 1 : -1
        });
      }
      
      // Add a few slightly larger stars
      for (let i = 0; i < 20; i++) {
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 2 + 1,
          baseOpacity: Math.random() * 0.7 + 0.3,
          opacity: Math.random() * 0.7 + 0.3,
          speed: Math.random() * 0.03 + 0.02,
          twinkleDirection: Math.random() > 0.5 ? 1 : -1
        });
      }
      
      return stars;
    }
    
    // Set canvas size to match parent
    const resizeCanvas = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      starsRef.current = generateStars();  // Regenerate stars after resize
    };
    
    // Animation function
    function animateStars() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw and animate each star
      starsRef.current.forEach(star => {
        // Update opacity for twinkling effect
        star.opacity += star.speed * star.twinkleDirection;
        
        // Change direction when reaching opacity bounds
        if (star.opacity <= 0.1 || star.opacity >= star.baseOpacity + 0.3) {
          star.twinkleDirection *= -1;
        }
        
        // Draw the star
        ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fill();
      });
      
      animationRef.current = requestAnimationFrame(animateStars);
    }
    
    // Set up event listeners
    window.addEventListener('resize', resizeCanvas);
    
    // Initialize canvas and start animation
    resizeCanvas();
    animateStars();
    
    // Cleanup function
    return () => {
      cancelAnimationFrame(animationRef.current);
      window.removeEventListener('resize', resizeCanvas);
    };
  }, []);


    return (
        <div className="relative bg-slate-900 py-24 sm:py-48 overflow-hidden my-20">
            {/* Galaxy background with stars */}
            <canvas
                ref={canvasRef}
                className="absolute inset-0 w-full h-full"
            />
            <div className="absolute inset-0">
                <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))]
          from-slate-800 via-slate-900 to-black"></div>
            </div>

            <div className="relative z-10 max-w-3xl mx-auto px-4 sm:px-6 text-center">
                <h1 className="text-3xl font-medium text-white sm:text-4xl mb-6">
                    Black Hole Database Query Tool
                </h1>
                <p className="mt-2 mb-8 text-base text-slate-300 sm:text-lg max-w-2xl mx-auto">
                    Access and analyze astronomical data through a simple interface
                    designed for researchers and academic users.
                </p>
            </div>
        </div>
    )
}