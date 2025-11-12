/**
 * @component AuthPrimaryButton (cmp/button/auth-primary)
 * @description Enterprise-grade primary button with sophisticated loading states
 */

import { Button } from "../../ui/button";
import { Loader2, Check } from "lucide-react";
import { ButtonHTMLAttributes } from "react";

interface AuthPrimaryButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  isLoading?: boolean;
  isSuccess?: boolean;
  loadingText?: string;
  successText?: string;
  children: React.ReactNode;
}

export function AuthPrimaryButton({ 
  isLoading = false,
  isSuccess = false,
  loadingText = "Authenticating...",
  successText = "Success!",
  children,
  className = "",
  ...props
}: AuthPrimaryButtonProps) {
  return (
    <Button 
      {...props}
      className={`btn-press ${className}`}
      style={{
        height: 'var(--button-height)',
        width: '100%',
        borderRadius: 'var(--radius-md)',
        fontSize: 'var(--text-md)',
        fontWeight: 500,
        letterSpacing: 'var(--letter-spacing-normal)',
        backgroundColor: 'var(--iu-crimson)',
        color: 'var(--color-text-inverse)',
        boxShadow: 'var(--shadow-sm)',
        border: 'none',
        cursor: props.disabled ? 'not-allowed' : 'pointer',
        opacity: props.disabled && !isLoading && !isSuccess ? 0.6 : 1
      }}
      onMouseEnter={(e) => {
        if (!props.disabled && !isLoading && !isSuccess) {
          e.currentTarget.style.backgroundColor = 'var(--iu-crimson-dark)';
          e.currentTarget.style.boxShadow = 'var(--shadow-md)';
        }
      }}
      onMouseLeave={(e) => {
        if (!props.disabled) {
          e.currentTarget.style.backgroundColor = 'var(--iu-crimson)';
          e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
        }
      }}
    >
      {isLoading ? (
        <span 
          className="flex items-center justify-center gap-2"
          style={{ animation: 'fadeIn var(--transition-base)' }}
        >
          <Loader2 
            className="size-5 animate-spin" 
            style={{ 
              animation: 'spin 1s linear infinite'
            }} 
          />
          <style>{`
            @keyframes spin {
              from { transform: rotate(0deg); }
              to { transform: rotate(360deg); }
            }
          `}</style>
          {loadingText}
        </span>
      ) : isSuccess ? (
        <span 
          className="flex items-center justify-center gap-2 success-pulse"
          style={{
            animation: 'fadeInScale var(--transition-slow)'
          }}
        >
          <Check className="size-5" strokeWidth={3} />
          {successText}
        </span>
      ) : (
        <span style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          gap: 'var(--space-2)'
        }}>
          {children}
        </span>
      )}
    </Button>
  );
}
