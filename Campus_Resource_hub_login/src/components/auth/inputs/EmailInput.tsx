/**
 * @component EmailInput (cmp/input/email)
 * @description Enterprise-grade email input with real-time validation
 */

import { Input } from "../../ui/input";
import { Label } from "../../ui/label";
import { AlertCircle, CheckCircle2 } from "lucide-react";
import { useState, useEffect } from "react";

interface EmailInputProps {
  value: string;
  onChange: (value: string) => void;
  error?: boolean;
  disabled?: boolean;
  onBlur?: () => void;
  label?: string;
  placeholder?: string;
  required?: boolean;
  showValidation?: boolean;
}

export function EmailInput({ 
  value, 
  onChange, 
  error = false, 
  disabled = false,
  onBlur,
  label = "IU Email Address",
  placeholder = "you@iu.edu",
  required = false,
  showValidation = true
}: EmailInputProps) {
  const [touched, setTouched] = useState(false);
  const [isValid, setIsValid] = useState(false);
  
  useEffect(() => {
    if (value) {
      setIsValid(value.includes('@iu.edu') && value.length > 7);
    } else {
      setIsValid(false);
    }
  }, [value]);
  
  const showError = error && touched;
  const showSuccess = isValid && touched && showValidation;
  
  return (
    <div className="group" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
      <Label 
        htmlFor="email" 
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
          id="email" 
          type="email" 
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
            paddingRight: showSuccess || showError ? 'var(--space-10)' : 'var(--space-3)',
            borderColor: showError ? 'var(--color-border-error)' : 'var(--color-border-default)',
            backgroundColor: showError ? 'var(--color-bg-error)' : 'var(--color-bg-default)',
            boxShadow: 'var(--shadow-xs)'
          }}
          onBlur={(e) => {
            setTouched(true);
            onBlur?.();
          }}
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
        {showSuccess && (
          <div 
            className="absolute right-3 top-1/2 -translate-y-1/2"
            style={{ animation: 'fadeIn var(--transition-base)' }}
          >
            <CheckCircle2 className="size-5" style={{ color: 'var(--color-success)' }} />
          </div>
        )}
        {showError && (
          <div 
            className="absolute right-3 top-1/2 -translate-y-1/2"
            style={{ animation: 'fadeIn var(--transition-base)' }}
          >
            <AlertCircle className="size-5" style={{ color: 'var(--color-error)' }} />
          </div>
        )}
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
          Please enter a valid IU email address
        </p>
      )}
    </div>
  );
}
