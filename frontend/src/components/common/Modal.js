import React, { useEffect } from 'react';

const Modal = ({ 
  show, 
  onClose, 
  title, 
  children, 
  actions,
  size = 'md', // sm, md, lg, xl
  closeOnBackdropClick = true,
  closeOnEscape = true,
  scrollable = false
}) => {
  // Handle ESC key press
  useEffect(() => {
    if (!closeOnEscape) return;
    
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && show) {
        console.log('ESC key pressed, closing modal');
        onClose();
      }
    };

    if (show) {
      document.addEventListener('keydown', handleKeyDown);
    }
    
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [show, onClose, closeOnEscape]);

  // Handle backdrop click
  const handleBackdropClick = (e) => {
    if (!closeOnBackdropClick) return;
    
    if (
      e.target.classList.contains('modal') || 
      e.target.classList.contains('modal-backdrop')
    ) {
      console.log('Backdrop clicked, closing modal');
      onClose();
    }
  };

  if (!show) return null;

  // Determine modal size class
  const sizeClass = {
    sm: 'modal-sm',
    md: '',
    lg: 'modal-lg',
    xl: 'modal-xl'
  }[size] || '';

  return (
    <div className="modal-wrapper">
      <div 
        className="modal fade show" 
        style={{ display: 'block' }} 
        tabIndex="-1"
        onClick={handleBackdropClick}
      >
        <div 
          className={`modal-dialog ${sizeClass} ${scrollable ? 'modal-dialog-scrollable' : ''}`}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="modal-content">
            {title && (
              <div className="modal-header">
                <h5 className="modal-title">{title}</h5>
                <button 
                  type="button" 
                  className="btn-close" 
                  onClick={onClose}
                  aria-label="Close"
                ></button>
              </div>
            )}
            
            <div className="modal-body">
              {children}
            </div>
            
            {actions && (
              <div className="modal-footer">
                {actions}
              </div>
            )}
          </div>
        </div>
      </div>
      <div 
        className="modal-backdrop fade show" 
        onClick={closeOnBackdropClick ? onClose : undefined}
      ></div>
    </div>
  );
};

export default Modal;