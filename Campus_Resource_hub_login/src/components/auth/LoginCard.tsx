/**
 * @component LoginCard (cmp/form/login-card)
 * @description Enterprise-grade login form card
 */

import { Checkbox } from "../ui/checkbox";
import { useState, FormEvent } from "react";
import { EmailInput } from "./inputs/EmailInput";
import { PasswordInput } from "./inputs/PasswordInput";
import { AuthPrimaryButton } from "./buttons/AuthPrimaryButton";
import { InlineLink } from "./links/InlineLink";
import { FormFeedbackAlert } from "./alerts/FormFeedbackAlert";

interface LoginCardProps {
  onNavigateToSignUp?: () => void;
  onSuccess?: (data: { email: string }) => void;
}

export function LoginCard({ onNavigateToSignUp, onSuccess }: LoginCardProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [emailError, setEmailError] = useState(false);
  const [showErrorBanner, setShowErrorBanner] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    
    // Validate email
    if (!email.includes('@iu.edu')) {
      setEmailError(true);
      setShowErrorBanner(true);
      return;
    }

    // Start loading
    setIsLoading(true);
    setShowErrorBanner(false);
    setEmailError(false);
    
    // Simulate authentication
    setTimeout(() => {
      setIsLoading(false);
      setIsSuccess(true);
      
      setTimeout(() => {
        onSuccess?.({ email });
      }, 800);
    }, 1800);
  };

  return (
    <div 
      style={{
        width: '480px',
        minHeight: '520px',
        borderRadius: 'var(--radius-lg)',
        backgroundColor: 'var(--color-bg-default)',
        padding: 'var(--space-8)',
        boxShadow: 'var(--shadow-md)',
        animation: 'fadeInScale var(--transition-slow)'
      }}
    >
      {/* Title Block */}
      <div style={{ marginBottom: 'var(--space-8)' }}>
        <h2 
          style={{ 
            fontSize: 'var(--text-2xl)', 
            fontWeight: 600,
            color: 'var(--color-text-primary)',
            marginBottom: 'var(--space-2)',
            letterSpacing: 'var(--letter-spacing-tight)'
          }}
        >
          Welcome Back
        </h2>
        <p 
          style={{ 
            fontSize: 'var(--text-md)', 
            color: 'var(--color-text-secondary)',
            lineHeight: 'var(--line-height-relaxed)'
          }}
        >
          Sign in to access your campus resources and bookings.
        </p>
      </div>

      {/* Error Banner */}
      {showErrorBanner && (
        <div style={{ marginBottom: 'var(--space-4)' }}>
          <FormFeedbackAlert variant="error" dismissible onDismiss={() => setShowErrorBanner(false)}>
            Invalid credentials. Please check your email and password.
          </FormFeedbackAlert>
        </div>
      )}
      
      {/* Form */}
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
          <EmailInput
            value={email}
            onChange={setEmail}
            error={emailError}
            disabled={isLoading || isSuccess}
            required
            showValidation
          />
          
          <PasswordInput
            value={password}
            onChange={setPassword}
            disabled={isLoading || isSuccess}
            required
          />
        </div>
        
        {/* Remember Me & Forgot Password */}
        <div 
          style={{ 
            marginTop: 'var(--space-4)', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-between' 
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
            <Checkbox 
              id="remember" 
              disabled={isLoading || isSuccess}
              checked={rememberMe}
              onCheckedChange={(checked) => setRememberMe(checked === true)}
              style={{
                borderColor: 'var(--color-border-default)',
                borderRadius: 'var(--radius-sm)'
              }}
            />
            <label
              htmlFor="remember"
              style={{ 
                fontSize: 'var(--text-base)', 
                color: 'var(--color-text-secondary)',
                cursor: 'pointer',
                userSelect: 'none'
              }}
            >
              Remember me
            </label>
          </div>
          <InlineLink href="#" variant="primary">
            Forgot password?
          </InlineLink>
        </div>
        
        {/* Login Button */}
        <div style={{ marginTop: 'var(--space-6)' }}>
          <AuthPrimaryButton
            type="submit"
            isLoading={isLoading}
            isSuccess={isSuccess}
            disabled={isLoading || isSuccess}
            loadingText="Signing in..."
            successText="Welcome!"
          >
            Sign In
          </AuthPrimaryButton>
        </div>
        
        {/* Sign Up Link */}
        <div style={{ marginTop: 'var(--space-4)', textAlign: 'center' }}>
          <span style={{ fontSize: 'var(--text-base)', color: 'var(--color-text-secondary)' }}>
            Don't have an account?{' '}
          </span>
          <InlineLink 
            href="#" 
            variant="primary"
            onClick={(e) => {
              e.preventDefault();
              onNavigateToSignUp?.();
            }}
          >
            Create one
          </InlineLink>
        </div>
      </form>
    </div>
  );
}
