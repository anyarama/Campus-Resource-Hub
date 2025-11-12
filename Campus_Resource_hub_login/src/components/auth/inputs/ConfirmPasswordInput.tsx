/**
 * @component ConfirmPasswordInput (cmp/input/confirm-password)
 * @description Enterprise-grade password confirmation with real-time matching
 */

import { Input } from "../../ui/input";
import { Label } from "../../ui/label";
import { Eye, EyeOff, AlertCircle, CheckCircle2 } from "lucide-react";
import { useState, useEffect } from "react";

interface ConfirmPasswordInputProps {
  value: string;
  onChange: (value: string) => void;
  error?: boolean;
  disabled?: boolean;
  label?: string;
  placeholder?: string;
  required?: boolean;
  originalPassword?: string;
}

export function ConfirmPasswordInput({ 
  value, 
  onChange, 
  error = false,
  disabled = false,
  label = "Confirm Password",
  placeholder = "Re-enter password",
  required = false,
  originalPassword = ""
}: ConfirmPasswordInputProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [touched, setTouched] = useState(false);
  const [isMatching, setIsMatching] = useState(false);
  
  useEffect(() => {
    if (value && originalPassword) {
      setIsMatching(value === originalPassword);
    } else {
      setIsMatching(false);
    }
  }, [value, originalPassword]);
  
  const showError = (error || (touched && value && !isMatching)) && value.length > 0;
  const showSuccess = isMatching && touched && value.length > 0;

  return (
    <div className="group" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
      <Label 
        htmlFor="confirmPassword" 
        style={{ 
          fontSize: 'var(--text-base)', 
          color: 'var(--color-text-primary)',
          fontWeight: 500,
          letterSpacing: 'var(--letter-spacing-normal)'
        }}
      >
        {label}
        {required && <span style={{ color: 'var(--color-error)', marginLeft: 'var(--space-1)' }}>*</span>}
      </Label>
      <div className="relative">
        <Input 
          id="confirmPassword" 
          type={showPassword ? "text" : "password"}
          placeholder={placeholder}
          value={value}
          onChange={(e) => {
            onChange(e.target.value);
            if (!touched) setTouched(true);
          }}
          disabled={disabled}
          className="input-glow transition-all"
          style={{
            height: 'var(--input-height)',
            borderRadius: 'var(--radius-md)',
            fontSize: 'var(--text-md)',
            paddingRight: 'var(--space-10)',
            borderColor: showError ? 'var(--color-border-error)' : 'var(--color-border-default)',
            backgroundColor: showError ? 'var(--color-bg-error)' : 'var(--color-bg-default)',
            boxShadow: 'var(--shadow-xs)'
          }}
          onBlur={() => setTouched(true)}
          onFocus={(e) => {
            e.target.style.boxShadow = showError 
              ? '0 0 0 3px var(--focus-ring-error), var(--shadow-sm)' 
              : '0 0 0 3px var(--focus-ring-color), var(--shadow-sm)';
            e.target.style.borderColor = showError ? 'var(--color-error)' : 'var(--iu-crimson)';
          }}
          onBlurCapture={(e) => {
            e.target.style.boxShadow = 'var(--shadow-xs)';
            e.target.style.borderColor = showError ? 'var(--color-border-error)' : 'var(--color-border-default)';
          }}
        />
        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
          {showSuccess && (
            <div style={{ animation: 'fadeIn var(--transition-base)' }}>
              <CheckCircle2 className="size-5" style={{ color: 'var(--color-success)' }} />
            </div>
          )}
          {showError && (
            <div style={{ animation: 'fadeIn var(--transition-base)' }}>
              <AlertCircle className="size-5" style={{ color: 'var(--color-error)' }} />
            </div>
          )}
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            disabled={disabled}
            className="transition-colors"
            style={{
              color: 'var(--color-text-secondary)',
              cursor: 'pointer',
              marginLeft: showSuccess || showError ? 'var(--space-1)' : '0'
            }}
            onMouseEnter={(e) => e.currentTarget.style.color = 'var(--color-text-primary)'}
            onMouseLeave={(e) => e.currentTarget.style.color = 'var(--color-text-secondary)'}
          >
            {showPassword ? (
              <EyeOff className="size-5" />
            ) : (
              <Eye className="size-5" />
            )}
          </button>
        </div>
      </div>
      {showError && (
        <p 
          style={{ 
            fontSize: 'var(--text-sm)', 
            color: 'var(--color-error)',
            animation: 'slideDown var(--transition-base)',
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-1)'
          }}
        >
          Passwords do not match
        </p>
      )}
    </div>
  );
}
