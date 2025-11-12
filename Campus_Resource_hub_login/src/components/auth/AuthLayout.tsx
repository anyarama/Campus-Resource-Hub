/**
 * @component AuthLayout
 * @description Enterprise-grade authentication layout with branding
 */

import { ImageWithFallback } from "../figma/ImageWithFallback";
import { ReactNode } from "react";

interface AuthLayoutProps {
  children: ReactNode;
  showSuccessToast?: boolean;
  successMessage?: string;
}

export function AuthLayout({ children, showSuccessToast, successMessage }: AuthLayoutProps) {
  return (
    <div 
      className="flex overflow-hidden"
      style={{
        width: '1440px',
        height: '1024px'
      }}
    >
      {/* Left Column - Branding */}
      <div 
        className="relative"
        style={{
          width: '480px',
          height: '100%',
          backgroundColor: 'var(--iu-crimson)',
          overflow: 'hidden'
        }}
      >
        {/* Background Image with Overlay */}
        <div className="absolute inset-0">
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1680226426952-514723cee6b8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx1bml2ZXJzaXR5JTIwY2FtcHVzJTIwYnVpbGRpbmd8ZW58MXx8fHwxNzYyODE5NDY3fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
            alt="Indiana University Campus"
            className="h-full w-full object-cover"
            style={{ opacity: 0.08 }}
          />
        </div>
        
        {/* Gradient Overlays */}
        <div 
          className="absolute inset-0" 
          style={{
            background: 'linear-gradient(135deg, rgba(0, 0, 0, 0.05) 0%, transparent 50%, rgba(255, 255, 255, 0.03) 100%)'
          }}
        />
        
        {/* Content */}
        <div 
          className="relative flex h-full flex-col items-center justify-center"
          style={{ padding: 'var(--space-16)' }}
        >
          {/* IU Trident Logo */}
          <div 
            style={{ 
              marginBottom: 'var(--space-6)',
              animation: 'fadeIn var(--transition-slower) ease-out'
            }}
          >
            <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path 
                d="M40 10V70M40 10L25 25M40 10L55 25M25 40H55M30 55L40 70L50 55" 
                stroke="white" 
                strokeWidth="3.5" 
                strokeLinecap="round" 
                strokeLinejoin="round"
                style={{ 
                  filter: 'drop-shadow(0 2px 8px rgba(0, 0, 0, 0.15))'
                }}
              />
            </svg>
          </div>
          
          {/* Indiana University Label */}
          <p 
            style={{
              color: 'rgba(255, 255, 255, 0.95)',
              fontSize: 'var(--text-sm)',
              letterSpacing: 'var(--letter-spacing-wide)',
              textTransform: 'uppercase',
              marginBottom: 'var(--space-4)',
              fontWeight: 500,
              animation: 'fadeIn var(--transition-slower) 100ms ease-out'
            }}
          >
            Indiana University
          </p>
          
          {/* Campus Resource Hub Title */}
          <h2 
            style={{ 
              color: 'white',
              fontSize: 'var(--text-2xl)',
              fontWeight: 600,
              textAlign: 'center',
              lineHeight: 'var(--line-height-normal)',
              letterSpacing: 'var(--letter-spacing-tight)',
              maxWidth: '320px',
              textShadow: '0 2px 12px rgba(0, 0, 0, 0.1)',
              animation: 'fadeIn var(--transition-slower) 200ms ease-out'
            }}
          >
            Campus Resource Hub
          </h2>
          
          {/* Tagline */}
          <p
            style={{
              color: 'rgba(255, 255, 255, 0.85)',
              fontSize: 'var(--text-md)',
              textAlign: 'center',
              marginTop: 'var(--space-3)',
              lineHeight: 'var(--line-height-relaxed)',
              maxWidth: '360px',
              animation: 'fadeIn var(--transition-slower) 300ms ease-out'
            }}
          >
            Streamline campus resource booking and management
          </p>
        </div>
      </div>
      
      {/* Right Column - Content Area */}
      <div 
        className="relative"
        style={{
          flex: 1,
          height: '100%',
          backgroundColor: 'var(--iu-cream)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 'var(--space-8)'
        }}
      >
        {/* Success Toast Notification */}
        {showSuccessToast && (
          <div
            style={{
              position: 'absolute',
              top: 'var(--space-8)',
              left: '50%',
              transform: 'translateX(-50%)',
              zIndex: 50,
              minWidth: '400px',
              maxWidth: '500px',
              animation: 'slideDown var(--transition-slow)',
              backgroundColor: 'var(--color-bg-default)',
              borderRadius: 'var(--radius-md)',
              boxShadow: 'var(--shadow-xl)',
              padding: 'var(--space-4)',
              borderLeft: '4px solid var(--color-success)'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
              <div 
                className="success-pulse"
                style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: 'var(--radius-full)',
                  backgroundColor: 'var(--color-bg-success)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}
              >
                <svg 
                  width="20" 
                  height="20" 
                  viewBox="0 0 20 20" 
                  fill="none" 
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path 
                    d="M16.6667 5L7.5 14.1667L3.33334 10" 
                    stroke="var(--color-success)" 
                    strokeWidth="2.5" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
              <div style={{ flex: 1 }}>
                <p 
                  style={{ 
                    fontSize: 'var(--text-md)', 
                    fontWeight: 600,
                    color: 'var(--color-text-primary)',
                    marginBottom: 'var(--space-1)'
                  }}
                >
                  {successMessage || 'Authentication Successful'}
                </p>
                <p 
                  style={{ 
                    fontSize: 'var(--text-base)', 
                    color: 'var(--color-text-secondary)'
                  }}
                >
                  Redirecting to your dashboard...
                </p>
              </div>
            </div>
          </div>
        )}
        
        {/* Content */}
        <div style={{ width: '100%', maxWidth: '600px' }}>
          {children}
        </div>
      </div>
    </div>
  );
}
