import { InputHTMLAttributes, ReactNode, useState, forwardRef } from 'react'
import { RiEyeLine, RiEyeOffLine } from '@remixicon/react'

interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string
  error?: string
  hint?: string
  variant?: 'default' | 'error' | 'success'
  size?: 'sm' | 'md' | 'lg'
  leftIcon?: ReactNode
  rightIcon?: ReactNode
  fullWidth?: boolean
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      hint,
      variant = 'default',
      size = 'md',
      leftIcon,
      rightIcon,
      fullWidth = true,
      className = '',
      type,
      disabled,
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = useState(false)
    const isPassword = type === 'password'
    const inputType = isPassword && showPassword ? 'text' : type

    const baseStyles =
      'block rounded-lg border transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-0 disabled:bg-gray-100 disabled:cursor-not-allowed'

    const variantStyles = {
      default: 'border-gray-300 focus:border-primary-500 focus:ring-primary-500',
      error: 'border-error-500 focus:border-error-500 focus:ring-error-500 text-error-900',
      success: 'border-success-500 focus:border-success-500 focus:ring-success-500',
    }

    const sizeStyles = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-5 py-3 text-lg',
    }

    const iconSizeStyles = {
      sm: 'w-4 h-4',
      md: 'w-5 h-5',
      lg: 'w-6 h-6',
    }

    // Determine variant based on error
    const effectiveVariant = error ? 'error' : variant

    const inputClassName = `
      ${baseStyles}
      ${variantStyles[effectiveVariant]}
      ${sizeStyles[size]}
      ${leftIcon ? 'pl-10' : ''}
      ${rightIcon || isPassword ? 'pr-10' : ''}
      ${fullWidth ? 'w-full' : ''}
      ${className}
    `

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {label}
          </label>
        )}

        <div className="relative">
          {leftIcon && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
              <span className={iconSizeStyles[size]}>{leftIcon}</span>
            </div>
          )}

          <input
            ref={ref}
            type={inputType}
            className={inputClassName}
            disabled={disabled}
            {...props}
          />

          {isPassword && (
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              tabIndex={-1}
            >
              {showPassword ? (
                <RiEyeOffLine className={iconSizeStyles[size]} />
              ) : (
                <RiEyeLine className={iconSizeStyles[size]} />
              )}
            </button>
          )}

          {rightIcon && !isPassword && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-gray-400">
              <span className={iconSizeStyles[size]}>{rightIcon}</span>
            </div>
          )}
        </div>

        {error && (
          <p className="mt-1 text-sm text-error-600">{error}</p>
        )}

        {hint && !error && (
          <p className="mt-1 text-sm text-gray-500">{hint}</p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

// Textarea component with similar styling
interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  hint?: string
  variant?: 'default' | 'error' | 'success'
  fullWidth?: boolean
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  (
    {
      label,
      error,
      hint,
      variant = 'default',
      fullWidth = true,
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      'block rounded-lg border px-4 py-2 text-base transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-0 disabled:bg-gray-100 disabled:cursor-not-allowed resize-y'

    const variantStyles = {
      default: 'border-gray-300 focus:border-primary-500 focus:ring-primary-500',
      error: 'border-error-500 focus:border-error-500 focus:ring-error-500 text-error-900',
      success: 'border-success-500 focus:border-success-500 focus:ring-success-500',
    }

    const effectiveVariant = error ? 'error' : variant

    const textareaClassName = `
      ${baseStyles}
      ${variantStyles[effectiveVariant]}
      ${fullWidth ? 'w-full' : ''}
      ${className}
    `

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {label}
          </label>
        )}

        <textarea
          ref={ref}
          className={textareaClassName}
          disabled={disabled}
          {...props}
        />

        {error && (
          <p className="mt-1 text-sm text-error-600">{error}</p>
        )}

        {hint && !error && (
          <p className="mt-1 text-sm text-gray-500">{hint}</p>
        )}
      </div>
    )
  }
)

Textarea.displayName = 'Textarea'

// Select component with similar styling
interface SelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'size'> {
  label?: string
  error?: string
  hint?: string
  variant?: 'default' | 'error' | 'success'
  size?: 'sm' | 'md' | 'lg'
  fullWidth?: boolean
  options: Array<{ value: string; label: string }>
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  (
    {
      label,
      error,
      hint,
      variant = 'default',
      size = 'md',
      fullWidth = true,
      options,
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      'block rounded-lg border transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-0 disabled:bg-gray-100 disabled:cursor-not-allowed appearance-none bg-white'

    const variantStyles = {
      default: 'border-gray-300 focus:border-primary-500 focus:ring-primary-500',
      error: 'border-error-500 focus:border-error-500 focus:ring-error-500 text-error-900',
      success: 'border-success-500 focus:border-success-500 focus:ring-success-500',
    }

    const sizeStyles = {
      sm: 'px-3 py-1.5 text-sm pr-8',
      md: 'px-4 py-2 text-base pr-10',
      lg: 'px-5 py-3 text-lg pr-12',
    }

    const effectiveVariant = error ? 'error' : variant

    const selectClassName = `
      ${baseStyles}
      ${variantStyles[effectiveVariant]}
      ${sizeStyles[size]}
      ${fullWidth ? 'w-full' : ''}
      ${className}
    `

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {label}
          </label>
        )}

        <div className="relative">
          <select
            ref={ref}
            className={selectClassName}
            disabled={disabled}
            {...props}
          >
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>

          <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            <svg
              className="w-4 h-4 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </div>
        </div>

        {error && (
          <p className="mt-1 text-sm text-error-600">{error}</p>
        )}

        {hint && !error && (
          <p className="mt-1 text-sm text-gray-500">{hint}</p>
        )}
      </div>
    )
  }
)

Select.displayName = 'Select'
