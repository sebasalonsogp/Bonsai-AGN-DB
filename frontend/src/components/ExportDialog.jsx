import { useState, useEffect, useRef } from 'react';
import { searchApi } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

// Function to get columns in a consistent order
const getOrderedColumns = (columns) => {
  // Define preferred order for important columns
  const preferredOrder = [
    'agn_id', 'ra', 'declination',  // Source columns first
    'redshift_type', 'z_value', 'z_error',  // Then redshift
    'spec_class', 'gen_class', 'xray_class', 'best_class', 'image_class', 'sed_class',  // Classifications
    'band_label', 'filter_name', 'mag_value', 'mag_error', 'extinction'  // Photometry at the end
  ];
  
  // Sort columns by preferred order first, then alphabetically for any remaining
  return [...columns].sort((a, b) => {
    const indexA = preferredOrder.indexOf(a);
    const indexB = preferredOrder.indexOf(b);
    
    // If both are in preferred order, use that order
    if (indexA >= 0 && indexB >= 0) {
      return indexA - indexB;
    }
    
    // If only one is in preferred order, prioritize it
    if (indexA >= 0) return -1;
    if (indexB >= 0) return 1;
    
    // Otherwise sort alphabetically
    return a.localeCompare(b);
  });
};

export default function ExportDialog({ isOpen, onClose, query, visibleColumns, sortField = null, sortDirection = 'asc' }) {
  const [format, setFormat] = useState('csv');
  const [includeMetadata, setIncludeMetadata] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableFields, setAvailableFields] = useState({ categories: {}, all_fields: [] });
  const [selectedFields, setSelectedFields] = useState([]);
  const [fieldsFetched, setFieldsFetched] = useState(false);
  
  // Track export process
  const [exportProgress, setExportProgress] = useState(0);
  const [exportTakingTooLong, setExportTakingTooLong] = useState(false);
  const exportTimeoutRef = useRef(null);
  const exportRequestRef = useRef(null);
  
  // Export formats
  const formats = [
    { id: 'csv', name: 'CSV (Comma Separated Values)' },
    { id: 'votable', name: 'VOTable (Virtual Observatory Table)' },
  ];
  
  // Load available fields when dialog opens
  useEffect(() => {
    if (isOpen && !fieldsFetched) {
      fetchAvailableFields();
    }
  }, [isOpen, fieldsFetched]);
  
  // Set visible columns as initially selected fields
  useEffect(() => {
    if (isOpen && visibleColumns) {
      const initialSelectedFields = Object.keys(visibleColumns)
        .filter(column => visibleColumns[column]);
      setSelectedFields(initialSelectedFields);
    }
  }, [isOpen, visibleColumns]);
  
  // Fetch available fields from the API
  const fetchAvailableFields = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const fields = await searchApi.getAvailableFields();
      setAvailableFields(fields);
      setFieldsFetched(true);
    } catch (err) {
      console.error('Failed to fetch fields:', err);
      setError('Failed to load available fields. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  // Handle export
  const handleExport = async () => {
    setLoading(true);
    setError(null);
    setExportProgress(0);
    setExportTakingTooLong(false);
    
    // Set a timeout for long export operations
    exportTimeoutRef.current = setTimeout(() => {
      setExportTakingTooLong(true);
    }, 5000); // Show message after 5 seconds
    
    try {
      const exportOptions = {
        format,
        selected_fields: selectedFields.length > 0 ? selectedFields : null,
        include_metadata: includeMetadata
      };
      
      // If the export is cancellable, store the reference
      const { promise, cancel } = searchApi.exportResultsWithCancellation(
        query, 
        exportOptions, 
        sortField, 
        sortDirection
      );
      
      exportRequestRef.current = { cancel };
      
      await promise;
      onClose();
    } catch (err) {
      console.error('Export failed:', err);
      setError(err);
    } finally {
      clearTimeout(exportTimeoutRef.current);
      setLoading(false);
      setExportTakingTooLong(false);
      exportRequestRef.current = null;
    }
  };
  
  // Handle cancellation
  const handleCancelExport = () => {
    if (exportRequestRef.current) {
      exportRequestRef.current.cancel();
      exportRequestRef.current = null;
    }
    clearTimeout(exportTimeoutRef.current);
    setLoading(false);
    setExportTakingTooLong(false);
    setError({ message: 'Export cancelled by user' });
  };
  
  // Toggle field selection
  const toggleField = (field) => {
    setSelectedFields(prev => 
      prev.includes(field)
        ? prev.filter(f => f !== field)
        : [...prev, field]
    );
  };
  
  // Select all fields in a category
  const selectCategory = (fields) => {
    setSelectedFields(prev => {
      const newFields = [...prev];
      
      fields.forEach(field => {
        if (!newFields.includes(field)) {
          newFields.push(field);
        }
      });
      
      return newFields;
    });
  };
  
  // Deselect all fields in a category
  const deselectCategory = (fields) => {
    setSelectedFields(prev => 
      prev.filter(field => !fields.includes(field))
    );
  };
  
  // Check if all fields in a category are selected
  const isCategorySelected = (fields) => {
    return fields.every(field => selectedFields.includes(field));
  };
  
  // Check if some fields in a category are selected
  const isCategoryPartiallySelected = (fields) => {
    return fields.some(field => selectedFields.includes(field)) && 
           !fields.every(field => selectedFields.includes(field));
  };
  
  // Select or deselect all fields
  const toggleAllFields = () => {
    if (selectedFields.length === availableFields.all_fields.length) {
      setSelectedFields([]);
    } else {
      setSelectedFields([...availableFields.all_fields]);
    }
  };
  
  // Ensure categories are displayed in a consistent order
  const getOrderedCategories = () => {
    // Define preferred category order
    const categoryOrder = ['source', 'redshift', 'classification', 'photometry', 'other'];
    
    // Get categories from availableFields
    const categories = Object.keys(availableFields.categories);
    
    // Sort by predefined order
    return categories.sort((a, b) => {
      const indexA = categoryOrder.indexOf(a);
      const indexB = categoryOrder.indexOf(b);
      
      // If both categories are in the preferred order
      if (indexA >= 0 && indexB >= 0) {
        return indexA - indexB;
      }
      
      // If only one is in the preferred order
      if (indexA >= 0) return -1;
      if (indexB >= 0) return 1;
      
      // Otherwise alphabetically
      return a.localeCompare(b);
    });
  };

  // Ensure fields within categories are displayed in a consistent order
  const getOrderedFieldsForCategory = (category, fields) => {
    return getOrderedColumns(fields);
  };
  
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm bg-gray-700/40">
      <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-3xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Export Data</h2>
          <button 
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
            disabled={loading}
          >
            ✕
          </button>
        </div>
        
        {error && <ErrorMessage error={error} />}
        
        {exportTakingTooLong && !error && (
          <div className="bg-yellow-50 border border-yellow-400 text-yellow-800 px-4 py-3 rounded mb-4">
            <p className="font-medium">Export preparation is taking longer than expected.</p>
            <p className="text-sm">Large data exports may take time to prepare. Please wait while we process your request.</p>
          </div>
        )}
        
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Export Format</h3>
          <div className="flex flex-wrap gap-4">
            {formats.map((fmt) => (
              <label key={fmt.id} className="flex items-center">
                <input
                  type="radio"
                  name="format"
                  value={fmt.id}
                  checked={format === fmt.id}
                  onChange={() => setFormat(fmt.id)}
                  className="mr-2"
                />
                {fmt.name}
              </label>
            ))}
          </div>
        </div>
        
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-semibold">Fields to Include</h3>
            <button
              onClick={toggleAllFields}
              className="text-blue-600 hover:text-blue-800 text-sm"
            >
              {selectedFields.length === availableFields.all_fields.length ? 
                'Deselect All' : 'Select All'}
            </button>
          </div>
          
          {loading ? (
            <div className="py-4 text-center">Loading available fields...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {getOrderedCategories().map((category) => {
                const fields = availableFields.categories[category] || [];
                const orderedFields = getOrderedFieldsForCategory(category, fields);
                
                return (
                  <div key={category} className="border rounded p-3">
                    <div className="flex items-center mb-2">
                      <input
                        type="checkbox"
                        checked={isCategorySelected(fields)}
                        ref={el => {
                          if (el) {
                            el.indeterminate = isCategoryPartiallySelected(fields);
                          }
                        }}
                        onChange={() => {
                          if (isCategorySelected(fields)) {
                            deselectCategory(fields);
                          } else {
                            selectCategory(fields);
                          }
                        }}
                        className="mr-2"
                      />
                      <span className="font-semibold capitalize">{category}</span>
                    </div>
                    
                    <div className="pl-6 grid grid-cols-1 gap-1">
                      {orderedFields.map(field => (
                        <label key={field} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={selectedFields.includes(field)}
                            onChange={() => toggleField(field)}
                            className="mr-2"
                          />
                          {field}
                        </label>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
        
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Options</h3>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={includeMetadata}
              onChange={() => setIncludeMetadata(!includeMetadata)}
              className="mr-2"
            />
            Include metadata (timestamp, field info, record count)
          </label>
        </div>
        
        <div className="flex justify-end gap-3">
          {loading ? (
            <div className="flex space-x-3">
              <button
                onClick={handleCancelExport}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
              >
                Cancel
              </button>
              <div className="flex items-center space-x-2 bg-blue-50 px-4 py-2 rounded">
                <LoadingSpinner size="sm" />
                <span>Preparing export...</span>
              </div>
            </div>
          ) : (
            <>
              <button
                onClick={onClose}
                className="px-4 py-2 border border-gray-300 rounded bg-white hover:bg-gray-100"
              >
                Cancel
              </button>
              <button
                onClick={handleExport}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-blue-300"
                disabled={selectedFields.length === 0}
              >
                Export
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
} 