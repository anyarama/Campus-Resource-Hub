import { useState } from "react";
import { AuthLogin } from "./components/AuthLogin";
import { AuthSignUp } from "./components/AuthSignUp";
import { Button } from "./components/ui/button";

export default function App() {
  const [currentView, setCurrentView] = useState<"login" | "signup">("login");
  const [direction, setDirection] = useState<"left" | "right">("left");
  const [isTransitioning, setIsTransitioning] = useState(false);

  const handleNavigation = (view: "login" | "signup") => {
    if (view === currentView || isTransitioning) return;
    
    setIsTransitioning(true);
    setDirection(view === "signup" ? "left" : "right");
    
    setTimeout(() => {
      setCurrentView(view);
      setIsTransitioning(false);
    }, 250);
  };

  return (
    <>
      <style>{`
        @keyframes slideInFromRight {
          from {
            transform: translateX(60px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        
        @keyframes slideInFromLeft {
          from {
            transform: translateX(-60px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        
        .slide-enter-left {
          animation: slideInFromRight var(--transition-slow) cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .slide-enter-right {
          animation: slideInFromLeft var(--transition-slow) cubic-bezier(0.4, 0, 0.2, 1);
        }
      `}</style>
      
      <div 
        style={{
          minHeight: '100vh',
          backgroundColor: '#f5f3f0',
          padding: 'var(--space-8)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 'var(--space-8)'
        }}
      >
        {/* Toggle Buttons */}
        <div 
          style={{ 
            display: 'flex', 
            gap: 'var(--space-3)',
            padding: 'var(--space-1)',
            backgroundColor: 'var(--color-bg-default)',
            borderRadius: 'var(--radius-md)',
            boxShadow: 'var(--shadow-sm)'
          }}
        >
          <Button
            onClick={() => handleNavigation("login")}
            variant={currentView === "login" ? "default" : "ghost"}
            style={{
              height: 'var(--input-height)',
              paddingLeft: 'var(--space-4)',
              paddingRight: 'var(--space-4)',
              borderRadius: 'var(--radius-sm)',
              fontSize: 'var(--text-base)',
              fontWeight: 500,
              backgroundColor: currentView === "login" ? 'var(--iu-crimson)' : 'transparent',
              color: currentView === "login" ? 'white' : 'var(--color-text-secondary)',
              transition: 'all var(--transition-base)'
            }}
            onMouseEnter={(e) => {
              if (currentView !== "login") {
                e.currentTarget.style.backgroundColor = 'var(--color-bg-hover)';
                e.currentTarget.style.color = 'var(--color-text-primary)';
              }
            }}
            onMouseLeave={(e) => {
              if (currentView !== "login") {
                e.currentTarget.style.backgroundColor = 'transparent';
                e.currentTarget.style.color = 'var(--color-text-secondary)';
              }
            }}
          >
            Login
          </Button>
          <Button
            onClick={() => handleNavigation("signup")}
            variant={currentView === "signup" ? "default" : "ghost"}
            style={{
              height: 'var(--input-height)',
              paddingLeft: 'var(--space-4)',
              paddingRight: 'var(--space-4)',
              borderRadius: 'var(--radius-sm)',
              fontSize: 'var(--text-base)',
              fontWeight: 500,
              backgroundColor: currentView === "signup" ? 'var(--iu-crimson)' : 'transparent',
              color: currentView === "signup" ? 'white' : 'var(--color-text-secondary)',
              transition: 'all var(--transition-base)'
            }}
            onMouseEnter={(e) => {
              if (currentView !== "signup") {
                e.currentTarget.style.backgroundColor = 'var(--color-bg-hover)';
                e.currentTarget.style.color = 'var(--color-text-primary)';
              }
            }}
            onMouseLeave={(e) => {
              if (currentView !== "signup") {
                e.currentTarget.style.backgroundColor = 'transparent';
                e.currentTarget.style.color = 'var(--color-text-secondary)';
              }
            }}
          >
            Sign Up
          </Button>
        </div>

        {/* Auth Frames */}
        <div 
          style={{
            boxShadow: 'var(--shadow-xl)',
            borderRadius: 'var(--radius-lg)',
            overflow: 'hidden'
          }}
        >
          <div
            key={currentView}
            className={`
              ${direction === "left" ? "slide-enter-left" : "slide-enter-right"}
            `}
          >
            {currentView === "login" ? (
              <AuthLogin onNavigateToSignUp={() => handleNavigation("signup")} />
            ) : (
              <AuthSignUp onNavigateToLogin={() => handleNavigation("login")} />
            )}
          </div>
        </div>
      </div>
    </>
  );
}