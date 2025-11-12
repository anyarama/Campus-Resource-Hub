/**
 * @component AuthSignUp
 * @description Enterprise-grade signup page
 */

import { useState } from "react";
import { AuthLayout } from "./auth/AuthLayout";
import { SignUpCard } from "./auth/SignUpCard";

interface AuthSignUpProps {
  onNavigateToLogin?: () => void;
}

export function AuthSignUp({ onNavigateToLogin }: AuthSignUpProps) {
  const [showSuccessToast, setShowSuccessToast] = useState(false);

  const handleSuccess = (data: { name: string; email: string; role: string }) => {
    setShowSuccessToast(true);
    
    // In a real app, this would redirect to email verification
    setTimeout(() => {
      console.log('Account created:', data);
    }, 2000);
  };

  return (
    <AuthLayout 
      showSuccessToast={showSuccessToast}
      successMessage="Account created successfully!"
    >
      <SignUpCard 
        onNavigateToLogin={onNavigateToLogin}
        onSuccess={handleSuccess}
      />
    </AuthLayout>
  );
}
