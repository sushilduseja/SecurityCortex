import React, { useState, useEffect, useRef } from 'react';
import { fetchReport } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';
import StatusBadge from '../common/StatusBadge';
import Modal from '../common/Modal';
import { gsap } from 'gsap';

// Improved markdown renderer that handles more markdown syntax
const MarkdownRenderer = ({ content }) => {
  if (!content) return null;
  
  // Process the content to create a structured representation of markdown elements
  const processMarkdown = (text) => {
    const elements = [];
    const lines = text.split('\n');
    
    let inList = false;
    let listItems = [];
    let listType = null;
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Handle headers
      if (line.startsWith('# ')) {
        if (inList) {
          elements.push(createList(listItems, listType));
          listItems = [];
          inList = false;
        }
        
        elements.push(
          <h1 key={`h1-${i}`} className="mt-4 mb-3 report-heading">
            {processInlineMarkdown(line.substring(2))}
          </h1>
        );
        continue;
      }
      
      if (line.startsWith('## ')) {
        if (inList) {
          elements.push(createList(listItems, listType));
          listItems = [];
          inList = false;
        }
        
        elements.push(
          <h2 key={`h2-${i}`} className="mt-3 mb-2 report-heading">
            {processInlineMarkdown(line.substring(3))}
          </h2>
        );
        continue;
      }
      
      if (line.startsWith('### ')) {
        if (inList) {
          elements.push(createList(listItems, listType));
          listItems = [];
          inList = false;
        }
        
        elements.push(
          <h3 key={`h3-${i}`} className="mt-3 mb-2 report-heading">
            {processInlineMarkdown(line.substring(4))}
          </h3>
        );
        continue;
      }
      
      // Handle unordered lists
      if (line.startsWith('- ') || line.startsWith('* ')) {
        const itemContent = line.startsWith('- ') ? line.substring(2) : line.substring(2);
        
        if (!inList || listType !== 'ul') {
          if (inList) {
            elements.push(createList(listItems, listType));
            listItems = [];
          }
          
          inList = true;
          listType = 'ul';
        }
        
        listItems.push(
          <li key={`li-${i}`} className="report-list-item">
            {processInlineMarkdown(itemContent)}
          </li>
        );
        continue;
      }
      
      // Handle ordered lists
      if (/^\d+\.\s/.test(line)) {
        const match = line.match(/^(\d+)\.\s(.*)$/);
        if (match) {
          const itemContent = match[2];
          
          if (!inList || listType !== 'ol') {
            if (inList) {
              elements.push(createList(listItems, listType));
              listItems = [];
            }
            
            inList = true;
            listType = 'ol';
          }
          
          listItems.push(
            <li key={`li-${i}`} className="report-list-item">
              {processInlineMarkdown(itemContent)}
            </li>
          );
          continue;
        }
      }
      
      // End of list
      if (inList && line.trim() === '') {
        elements.push(createList(listItems, listType));
        listItems = [];
        inList = false;
        elements.push(<br key={`br-${i}`} />);
        continue;
      }
      
      // Other content - process as paragraphs
      if (!inList && line.trim() !== '') {
        elements.push(
          <p key={`p-${i}`} className="mb-2 report-paragraph">
            {processInlineMarkdown(line)}
          </p>
        );
      } else if (!inList && line.trim() === '') {
        elements.push(<br key={`br-${i}`} />);
      }
    }
    
    // Add any remaining list items
    if (inList && listItems.length > 0) {
      elements.push(createList(listItems, listType));
    }
    
    return elements;
  };
  
  // Helper to create list elements
  const createList = (items, type) => {
    if (type === 'ul') {
      return <ul className="report-list mb-3">{items}</ul>;
    } else {
      return <ol className="report-list mb-3">{items}</ol>;
    }
  };
  
  // Process inline markdown elements like bold, italic, etc.
  const processInlineMarkdown = (text) => {
    if (!text) return '';
    
    // Process bold text (**text**)
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Process italic text (*text*)
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Process code blocks (`text`)
    text = text.replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Process links [text](url)
    text = text.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
    
    // Convert the processed text to React elements
    const parts = text.split(/(<[^>]+>.*?<\/[^>]+>)/);
    
    return parts.map((part, index) => {
      if (part.startsWith('<strong>')) {
        const content = part.replace(/<strong>(.*?)<\/strong>/, '$1');
        return <strong key={index}>{content}</strong>;
      } else if (part.startsWith('<em>')) {
        const content = part.replace(/<em>(.*?)<\/em>/, '$1');
        return <em key={index}>{content}</em>;
      } else if (part.startsWith('<code>')) {
        const content = part.replace(/<code>(.*?)<\/code>/, '$1');
        return <code key={index} className="bg-light px-1 rounded">{content}</code>;
      } else if (part.startsWith('<a')) {
        const matches = part.match(/<a href="(.*?)">(.*?)<\/a>/);
        if (matches) {
          return <a key={index} href={matches[1]} target="_blank" rel="noopener noreferrer">{matches[2]}</a>;
        }
        return part;
      } else {
        return part;
      }
    });
  };
  
  return <div className="markdown-content">{processMarkdown(content)}</div>;
};

const ReportDetailModal = ({ show, reportId, onClose }) => {
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const contentRef = useRef(null);

  useEffect(() => {
    const loadReport = async () => {
      if (!reportId || !show) return;
      
      try {
        setIsLoading(true);
        const data = await fetchReport(reportId);
        setReport(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching report details:', err);
        setError('Failed to load report details');
      } finally {
        setIsLoading(false);
      }
    };

    loadReport();
  }, [reportId, show]);
  
  // Animation effect when content becomes visible
  useEffect(() => {
    if (contentRef.current && report && !isLoading) {
      // Animate the content appearance
      gsap.fromTo(
        contentRef.current.querySelectorAll('.card, .row'),
        { 
          y: 20, 
          opacity: 0 
        },
        { 
          y: 0, 
          opacity: 1, 
          stagger: 0.1, 
          duration: 0.5,
          ease: 'power2.out'
        }
      );
      
      // Additional animation for headings
      gsap.fromTo(
        contentRef.current.querySelectorAll('.report-heading'),
        { 
          x: -10, 
          opacity: 0 
        },
        { 
          x: 0, 
          opacity: 1, 
          stagger: 0.05, 
          duration: 0.4,
          delay: 0.3
        }
      );
    }
  }, [report, isLoading]);
  
  // Format the report type to be more readable
  const formatReportType = (type) => {
    if (!type) return '';
    
    // Convert from snake_case or camelCase to Title Case with spaces
    return type
      .replace(/_/g, ' ')  // Replace underscores with spaces
      .replace(/([A-Z])/g, ' $1')  // Add space before capital letters
      .replace(/^\w/, c => c.toUpperCase())  // Capitalize first letter
      .trim();  // Remove any leading/trailing spaces
  };
  
  const modalContent = (
    <>
      {isLoading ? (
        <LoadingSpinner message="Loading report details..." />
      ) : error ? (
        <div className="alert alert-danger">
          <i className="fas fa-exclamation-circle me-2"></i>
          {error}
        </div>
      ) : report ? (
        <div ref={contentRef} className="report-details">
          <div className="row mb-4">
            <div className="col-md-8">
              <h2 className="report-title">{report.title}</h2>
              <p className="text-muted report-description">{report.description}</p>
            </div>
            <div className="col-md-4 text-md-end">
              <div className="mb-2">
                <StatusBadge status={report.status} />
              </div>
              <small className="text-muted">
                Type: {formatReportType(report.report_type)}
              </small>
            </div>
          </div>
          
          <div className="card mb-4 shadow-sm">
            <div className="card-header bg-light d-flex align-items-center">
              <i className="fas fa-lightbulb text-warning me-2"></i>
              <h6 className="mb-0">Report Insights</h6>
            </div>
            <div className="card-body bg-light">
              <div className="insights">
                <MarkdownRenderer content={report.insights} />
              </div>
            </div>
          </div>
          
          <div className="card mb-4 shadow-sm">
            <div className="card-header bg-light d-flex align-items-center">
              <i className="fas fa-file-alt text-primary me-2"></i>
              <h6 className="mb-0">Report Content</h6>
            </div>
            <div className="card-body">
              <div className="report-content">
                <MarkdownRenderer content={report.content} />
              </div>
            </div>
          </div>
          
          <div className="text-muted mt-3 d-flex align-items-center">
            <i className="far fa-calendar-alt me-2"></i>
            Report generated on {new Date(report.created_at).toLocaleString()}
          </div>
        </div>
      ) : (
        <div className="alert alert-warning">
          <i className="fas fa-exclamation-triangle me-2"></i>
          Report not found
        </div>
      )}
    </>
  );
  
  const modalActions = (
    <>
      <button 
        type="button" 
        className="btn btn-secondary" 
        onClick={onClose}
      >
        <i className="fas fa-times me-1"></i>
        Close
      </button>
      {report && (
        <button 
          type="button" 
          className="btn btn-primary"
        >
          <i className="fas fa-file-export me-1"></i>
          Export Report
        </button>
      )}
    </>
  );

  return (
    <Modal
      show={show}
      onClose={onClose}
      title={
        <div className="d-flex align-items-center">
          <i className="fas fa-chart-line text-primary me-2"></i>
          Report Details
        </div>
      }
      size="lg"
      actions={modalActions}
      closeOnBackdropClick={true}
      closeOnEscape={true}
      scrollable={true}
    >
      {modalContent}
    </Modal>
  );
};

export default ReportDetailModal;