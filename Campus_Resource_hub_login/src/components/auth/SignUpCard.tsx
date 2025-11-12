/**
 * @component SignUpCard (cmp/form/signup-card)
 * @description Enterprise-grade account creation form card
 */

import { Checkbox } from "../ui/checkbox";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { useState, FormEvent } from "react";
import { EmailInput } from "./inputs/EmailInput";
import { PasswordInput } from "./inputs/PasswordInput";
import { ConfirmPasswordInput } from "./inputs/ConfirmPasswordInput";
import { RoleSelect } from "./dropdowns/RoleSelect";
import { AuthPrimaryButton } from "./buttons/AuthPrimaryButton";
import { InlineLink } from "./links/InlineLink";
import { FormFeedbackAlert } from "./alerts/FormFeedbackAlert";

interface SignUpCardProps {
  onNavigateToLogin?: () => void;
  onSuccess?: (data: { name: string; email: string; role: string }) => void;
}

export function SignUpCard({ onNavigateToLogin, onSuccess }: SignUpCardProps) {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("");
  const [passwordMismatch, setPasswordMismatch] = useState(false);
  const [termsError, setTermsError] = useState(false);
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [showSuccessBanner, setShowSuccessBanner] = useState(false);
  const [showInfoBanner, setShowInfoBanner] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    
    // Validate passwords match
    if (password !== confirmPassword && password && confirmPassword) {
      setPasswordMismatch(true);
      return;
    }
    
    // Validate terms accepted
    if (!termsAccepted) {
      setTermsError(true);
      return;
    }

    // Start loading
    setIsLoading(true);
    setShowInfoBanner(false);
    
    // Simulate authentication
    setTimeout(() => {
      setIsLoading(false);
      setIsSuccess(true);
      
      setTimeout(() => {
        setShowSuccessBanner(true);
        setTimeout(() => {
          onSuccess?.({ name: fullName, email, role });
        }, 1500);
      }, 800);
    }, 1800);
  };

  return (
    <div 
      style={{
        width: '520px',
        borderRadius: 'var(--radius-lg)',
        backgroundColor: 'var(--color-bg-default)',
        padding: 'var(--space-8)',
        boxShadow: 'var(--shadow-md)',
        animation: 'fadeInScale var(--transition-slow)'
      }}
    >
      {/* Title Block */}
      <div style={{ marginBottom: 'var(--space-6)' }}>
        <h2 
          style={{ 
            fontSize: 'var(--text-2xl)', 
            fontWeight: 600,
            color: 'var(--color-text-primary)',
            marginBottom: 'var(--space-2)',
            letterSpacing: 'var(--letter-spacing-tight)'
          }}
        >
          Create Your Account
        </h2>
        <p 
          style={{ 
            fontSize: 'var(--text-md)', 
            color: 'var(--color-text-secondary)',
            lineHeight: 'var(--line-height-relaxed)'
          }}
        >
          Join Campus Resource Hub to book resources and manage requests.
        </p>
      </div>

      {/* Info Banner */}
      {showInfoBanner && (
        <div style={{ marginBottom: 'var(--space-4)' }}>
          <FormFeedbackAlert variant="info" dismissible onDismiss={() => setShowInfoBanner(false)}>
            Use your official IU email address to create an account.
          </FormFeedbackAlert>
        </div>
      )}

      {/* Success Banner */}
      {showSuccessBanner && (
        <div style={{ marginBottom: 'var(--space-4)' }}>
          <FormFeedbackAlert variant="success">
            Account created successfully! Check your email for verification.
          </FormFeedbackAlert>
        </div>
      )}
      
      {/* Form */}
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
            <Label 
              htmlFor="fullName" 
              style={{ 
                fontSize: 'var(--text-base)', 
                color: 'var(--color-text-primary)',
                fontWeight: 500
              }}
            >
              Full Name
              <span style={{ color: 'var(--color-error)', marginLeft: 'var(--space-1)' }}>*</span>
            </Label>
            <Input 
              id="fullName"
              type="text"
              placeholder="John Doe"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              disabled={isLoading || isSuccess}
              className="input-glow transition-all"
              style={{
                height: 'var(--input-height)',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--text-md)',
                borderColor: 'var(--color-border-default)',
                backgroundColor: 'var(--color-bg-default)',
                boxShadow: 'var(--shadow-xs)'
              }}
              onFocus={(e) => {
                e.target.style.boxShadow = '0 0 0 3px var(--focus-ring-color), var(--shadow-sm)';
                e.target.style.borderColor = 'var(--iu-crimson)';
              }}
              onBlur={(e) => {
                e.target.style.boxShadow = 'var(--shadow-xs)';
                e.target.style.borderColor = 'var(--color-border-default)';
              }}
            />
          </div>
          
          <EmailInput
            value={email}
            onChange={setEmail}
            disabled={isLoading || isSuccess}
            required
            showValidation
          />
          
          <PasswordInput
            value={password}
            onChange={(val) => {
              setPassword(val);
              setPasswordMismatch(false);
            }}
            disabled={isLoading || isSuccess}
            required
            showStrength
          />
          
          <ConfirmPasswordInput
            value={confirmPassword}
            onChange={(val) => {
              setConfirmPassword(val);
              setPasswordMismatch(false);
            }}
            error={passwordMismatch}
            disabled={isLoading || isSuccess}
            required
            originalPassword={password}
          />
          
          <RoleSelect
            value={role}
            onChange={setRole}
            disabled={isLoading || isSuccess}
            required
          />
        </div>
        
        {/* Terms Checkbox */}
        <div 
          style={{ 
            marginTop: 'var(--space-3)', 
            display: 'flex', 
            alignItems: 'start', 
            gap: 'var(--space-2)',
            padding: 'var(--space-3)',
            borderRadius: 'var(--radius-sm)',
            backgroundColor: termsError ? 'var(--color-bg-error)' : 'transparent',
            transition: 'background-color var(--transition-base)'
          }}
        >
          <Checkbox 
            id="terms" 
            disabled={isLoading || isSuccess}
            checked={termsAccepted}
            onCheckedChange={(checked) => {
              setTermsAccepted(checked === true);
              setTermsError(false);
            }}
            style={{
              marginTop: '2px',
              borderColor: termsError ? 'var(--color-border-error)' : 'var(--color-border-default)',
              borderRadius: 'var(--radius-sm)'
            }}
          />
          <label
            htmlFor="terms"
            style={{ 
              fontSize: 'var(--text-base)', 
              color: termsError ? 'var(--color-error)' : 'var(--color-text-secondary)',
              cursor: 'pointer',
              userSelect: 'none',
              lineHeight: 'var(--line-height-relaxed)'
            }}
          >
            I agree to the{' '}
            <InlineLink href="#" variant="primary">
              Campus Resource Usage Policy
            </InlineLink>
            {' '}and{' '}
            <InlineLink href="#" variant="primary">
              Terms of Service
            </InlineLink>
          </label>
        </div>
        {termsError && (
          <p 
            style={{ 
              marginTop: 'var(--space-2)',
              fontSize: 'var(--text-sm)', 
              color: 'var(--color-error)',
              animation: 'slideDown var(--transition-base)',
              paddingLeft: 'var(--space-6)'
            }}
          >
            Please accept the terms to continue
          </p>
        )}
        
        {/* Sign Up Button */}
        <div style={{ marginTop: 'var(--space-5)' }}>
          <AuthPrimaryButton
            type="submit"
            isLoading={isLoading}
            isSuccess={isSuccess}
            disabled={isLoading || isSuccess}
            loadingText="Creating account..."
            successText="Account created!"
          >
            Create Account
          </AuthPrimaryButton>
        </div>
        
        {/* Login Link */}
        <div style={{ marginTop: 'var(--space-3)', textAlign: 'center' }}>
          <span style={{ fontSize: 'var(--text-base)', color: 'var(--color-text-secondary)' }}>
            Already have an account?{' '}
          </span>
          <InlineLink 
            href="#" 
            variant="primary"
            onClick={(e) => {
              e.preventDefault();
              onNavigateToLogin?.();
            }}
          >
            Sign in
          </InlineLink>
        </div>
      </form>
    </div>
  );
}
