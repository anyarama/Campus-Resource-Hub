/**
 * @component AuthLogin
 * @description Enterprise-grade login page
 */

import { useState } from "react";
import { AuthLayout } from "./auth/AuthLayout";
import { LoginCard } from "./auth/LoginCard";
import { Check } from "lucide-react";

interface AuthLoginProps {
  onNavigateToSignUp?: () => void;
}

export function AuthLogin({ onNavigateToSignUp }: AuthLoginProps) {
  const [showSuccessToast, setShowSuccessToast] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);

  const handleSuccess = (data: { email: string }) => {
    setShowSuccessToast(true);
    
    // Redirect to dashboard after animation
    setTimeout(() => {
      setShowDashboard(true);
    }, 2000);
  };

  if (showDashboard) {
    return (
      <div 
        style={{
          width: '1440px',
          height: '1024px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'var(--iu-cream)',
          animation: 'fadeIn var(--transition-slower)'
        }}
      >
        <div style={{ textAlign: 'center', maxWidth: '800px' }}>
          <div 
            style={{ 
              marginBottom: 'var(--space-8)', 
              display: 'flex', 
              justifyContent: 'center',
              animation: 'fadeInScale var(--transition-slower)'
            }}
          >
            <div 
              className="success-pulse"
              style={{
                borderRadius: 'var(--radius-full)',
                backgroundColor: 'var(--color-bg-success)',
                padding: 'var(--space-6)'
              }}
            >
              <Check 
                style={{ 
                  width: '64px', 
                  height: '64px',
                  color: 'var(--color-success)',
                  strokeWidth: 3
                }} 
              />
            </div>
          </div>
          <h1 
            style={{ 
              fontSize: 'var(--text-3xl)', 
              fontWeight: 600,
              color: 'var(--color-text-primary)',
              marginBottom: 'var(--space-4)',
              letterSpacing: 'var(--letter-spacing-tight)'
            }}
          >
            Dashboard Preview
          </h1>
          <p 
            style={{ 
              fontSize: 'var(--text-md)', 
              color: 'var(--color-text-secondary)',
              lineHeight: 'var(--line-height-relaxed)',
              marginBottom: 'var(--space-8)'
            }}
          >
            Welcome back! Here's what's happening with your campus resources.
          </p>
          <div style={{ marginTop: 'var(--space-8)' }}>
            <div 
              style={{
                display: 'inline-flex',
                gap: 'var(--space-6)',
                borderRadius: 'var(--radius-lg)',
                border: '1px solid var(--color-border-default)',
                backgroundColor: 'var(--color-bg-default)',
                padding: 'var(--space-8)',
                boxShadow: 'var(--shadow-lg)',
                animation: 'fadeInScale var(--transition-slower) 200ms'
              }}
            >
              <div style={{ textAlign: 'left', minWidth: '140px' }}>
                <p 
                  style={{ 
                    fontSize: 'var(--text-base)', 
                    color: 'var(--color-text-secondary)',
                    marginBottom: 'var(--space-1)'
                  }}
                >
                  Total Bookings
                </p>
                <p 
                  style={{ 
                    fontSize: 'var(--text-3xl)', 
                    fontWeight: 600,
                    color: 'var(--color-text-primary)',
                    letterSpacing: 'var(--letter-spacing-tight)'
                  }}
                >
                  1,284
                </p>
              </div>
              <div 
                style={{ 
                  width: '1px', 
                  backgroundColor: 'var(--color-border-default)'
                }}
              />
              <div style={{ textAlign: 'left', minWidth: '140px' }}>
                <p 
                  style={{ 
                    fontSize: 'var(--text-base)', 
                    color: 'var(--color-text-secondary)',
                    marginBottom: 'var(--space-1)'
                  }}
                >
                  Active Users
                </p>
                <p 
                  style={{ 
                    fontSize: 'var(--text-3xl)', 
                    fontWeight: 600,
                    color: 'var(--color-text-primary)',
                    letterSpacing: 'var(--letter-spacing-tight)'
                  }}
                >
                  892
                </p>
              </div>
              <div 
                style={{ 
                  width: '1px', 
                  backgroundColor: 'var(--color-border-default)'
                }}
              />
              <div style={{ textAlign: 'left', minWidth: '140px' }}>
                <p 
                  style={{ 
                    fontSize: 'var(--text-base)', 
                    color: 'var(--color-text-secondary)',
                    marginBottom: 'var(--space-1)'
                  }}
                >
                  Resources
                </p>
                <p 
                  style={{ 
                    fontSize: 'var(--text-3xl)', 
                    fontWeight: 600,
                    color: 'var(--color-text-primary)',
                    letterSpacing: 'var(--letter-spacing-tight)'
                  }}
                >
                  156
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <AuthLayout 
      showSuccessToast={showSuccessToast}
      successMessage="Welcome back!"
    >
      <LoginCard 
        onNavigateToSignUp={onNavigateToSignUp}
        onSuccess={handleSuccess}
      />
    </AuthLayout>
  );
}
