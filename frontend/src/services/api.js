// API service for interacting with the backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Makes an API request with timeout and cancellation support
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Fetch options
 * @param {number} timeout - Request timeout in milliseconds (default: 60000)
 * @returns {Promise<any>} Response data
 */
async function apiRequest(endpoint, options = {}, timeout = 60000) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  // Create AbortController for cancellation if not provided
  const usedAbortController = options.signal?.abortController || new AbortController();
  const signal = usedAbortController.signal;
  
  // Setup timeout unless using an external controller
  let timeoutId;
  if (!options.signal) {
    timeoutId = setTimeout(() => {
      usedAbortController.abort();
    }, timeout);
  }
  
  try {
    const response = await fetch(url, {
      ...config,
      signal
    });
    
    // Handle non-JSON responses
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();
      
      if (!response.ok) {
        const error = new Error(data.message || 'An error occurred');
        error.status = response.status;
        error.details = data.detail || null;
        throw error;
      }
      
      return data;
    } else {
      if (!response.ok) {
        const error = new Error('An error occurred');
        error.status = response.status;
        throw error;
      }
      return await response.text();
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      const timeoutError = new Error('Query timed out. Please refine your search criteria to make the query less complex.');
      timeoutError.status = 408; // Request Timeout status
      throw timeoutError;
    }
    console.error('API request failed:', error);
    throw error;
  } finally {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  }
}

/**
 * Downloads a file from a blob
 * @param {Blob} blob - File blob
 * @param {string} filename - Suggested filename
 */
function downloadBlob(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

/**
 * API endpoints for sources
 */
export const sourcesApi = {
  /**
   * Get all sources with pagination
   * @param {Object} params - Query parameters
   * @returns {Promise<any>} Paginated sources
   */
  getSources: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`/sources/?${queryString}`);
  },
  
  /**
   * Get source by ID
   * @param {number} id - Source ID
   * @returns {Promise<any>} Source data
   */
  getSourceById: (id) => {
    return apiRequest(`/sources/${id}`);
  },
  
  /**
   * Search sources by coordinates
   * @param {Object} params - Coordinate search parameters
   * @returns {Promise<any>} Search results
   */
  searchByCoordinates: (params) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`/sources/coordinates?${queryString}`);
  }
};

/**
 * API endpoints for photometry
 */
export const photometryApi = {
  /**
   * Get photometry data with pagination
   * @param {Object} params - Query parameters
   * @returns {Promise<any>} Paginated photometry data
   */
  getPhotometry: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`/photometry/?${queryString}`);
  },
  
  /**
   * Get photometry by source ID
   * @param {number} sourceId - Source ID
   * @param {Object} params - Query parameters
   * @returns {Promise<any>} Photometry data for source
   */
  getPhotometryBySource: (sourceId, params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`/photometry/source/${sourceId}?${queryString}`);
  }
};

/**
 * API endpoints for redshift
 */
export const redshiftApi = {
  /**
   * Get redshift data with pagination
   * @param {Object} params - Query parameters
   * @returns {Promise<any>} Paginated redshift data
   */
  getRedshifts: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`/redshift/?${queryString}`);
  },
  
  /**
   * Get redshift by source ID
   * @param {number} sourceId - Source ID
   * @param {Object} params - Query parameters
   * @returns {Promise<any>} Redshift data for source
   */
  getRedshiftsBySource: (sourceId, params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`/redshift/source/${sourceId}?${queryString}`);
  }
};

/**
 * API endpoints for classifications
 */
export const classificationApi = {
  /**
   * Get classification data with pagination
   * @param {Object} params - Query parameters
   * @returns {Promise<any>} Paginated classification data
   */
  getClassifications: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`/classification/?${queryString}`);
  },
  
  /**
   * Get classification by source ID
   * @param {number} sourceId - Source ID
   * @returns {Promise<any>} Classification data for source
   */
  getClassificationBySource: (sourceId) => {
    return apiRequest(`/classification/source/${sourceId}`);
  }
};

/**
 * API endpoints for search
 */
export const searchApi = {
  /**
   * Execute a complex search query
   * @param {Object} query - Query parameters built from QueryBuilder
   * @param {Object} params - Pagination parameters
   * @param {string} params.sort_field - Field to sort by
   * @param {string} params.sort_direction - Sort direction (asc/desc)
   * @returns {Promise<any>} Search results
   */
  executeQuery: (query, params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`/search?${queryString}`, {
      method: 'POST',
      body: JSON.stringify(query)
    });
  },
  
  /**
   * Execute a complex search query with cancellation support
   * @param {Object} query - Query parameters built from QueryBuilder
   * @param {Object} params - Pagination parameters
   * @param {Object} options - Query options
   * @param {number} options.timeout - Request timeout in milliseconds
   * @returns {Object} - Contains the promise and a cancel function
   */
  executeQueryWithCancellation: (query, params = {}, options = {}) => {
    const controller = new AbortController();
    const timeout = options.timeout || 60000;
    
    const queryString = new URLSearchParams(params).toString();
    const promise = apiRequest(`/search?${queryString}`, {
      method: 'POST',
      body: JSON.stringify(query),
      signal: { abortController: controller }
    }, timeout);
    
    return {
      promise,
      cancel: () => controller.abort()
    };
  },
  
  /**
   * Get available fields for export
   * @returns {Promise<any>} Available fields data
   */
  getAvailableFields: () => {
    return apiRequest('/search/available-fields');
  },
  
  /**
   * Export search results in specified format
   * @param {Object} query - Query parameters built from QueryBuilder
   * @param {Object} exportOptions - Export options (format, fields, metadata)
   * @param {string} sortField - Field to sort by
   * @param {string} sortDirection - Sort direction (asc/desc)
   * @returns {Promise<void>} Initiates file download
   */
  exportResults: async (query, exportOptions, sortField = null, sortDirection = 'asc') => {
    try {
      // Build query parameters
      let queryParams = '';
      if (sortField) {
        queryParams = `?sort_field=${sortField}&sort_direction=${sortDirection}`;
      }
      
      const response = await fetch(`${API_BASE_URL}/search/export${queryParams}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          export_options: exportOptions
        })
      });
      
      if (!response.ok) {
        let errorMessage = 'Export failed';
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch (e) {
          // If parsing JSON fails, use the response text or status
          try {
            errorMessage = await response.text() || `Export failed with status ${response.status}`;
          } catch (e2) {
            // If that also fails, use status code
            errorMessage = `Export failed with status ${response.status}`;
          }
        }
        throw new Error(errorMessage);
      }
      
      // Get filename from content-disposition header or use default
      const contentDisposition = response.headers.get('content-disposition');
      let filename = 'export.csv';
      
      if (contentDisposition) {
        const match = contentDisposition.match(/filename=([^;]+)/);
        if (match) {
          filename = match[1].trim().replace(/"/g, '');
        }
      } else if (exportOptions.format === 'votable') {
        filename = 'agn_db_export.xml';
      }
      
      // Create and download blob
      const blob = await response.blob();
      downloadBlob(blob, filename);
      
      return true;
    } catch (error) {
      console.error('Export failed:', error);
      throw error;
    }
  },
  
  /**
   * Export search results with cancellation support
   * @param {Object} query - Query parameters built from QueryBuilder
   * @param {Object} exportOptions - Export options (format, fields, metadata)
   * @param {string} sortField - Field to sort by
   * @param {string} sortDirection - Sort direction (asc/desc)
   * @returns {Object} Contains the promise and a cancel function
   */
  exportResultsWithCancellation: (query, exportOptions, sortField = null, sortDirection = 'asc') => {
    const controller = new AbortController();
    const signal = controller.signal;
    
    // Build query parameters
    let queryParams = '';
    if (sortField) {
      queryParams = `?sort_field=${sortField}&sort_direction=${sortDirection}`;
    }
    
    const promise = (async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/search/export${queryParams}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query,
            export_options: exportOptions
          }),
          signal
        });
        
        if (!response.ok) {
          let errorMessage = 'Export failed';
          try {
            const errorData = await response.json();
            errorMessage = errorData.message || errorMessage;
          } catch (e) {
            // If parsing JSON fails, use the response text or status
            try {
              errorMessage = await response.text() || `Export failed with status ${response.status}`;
            } catch (e2) {
              // If that also fails, use status code
              errorMessage = `Export failed with status ${response.status}`;
            }
          }
          throw new Error(errorMessage);
        }
        
        // Get filename from content-disposition header or use default
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'export.csv';
        
        if (contentDisposition) {
          const match = contentDisposition.match(/filename=([^;]+)/);
          if (match) {
            filename = match[1].trim().replace(/"/g, '');
          }
        } else if (exportOptions.format === 'votable') {
          filename = 'agn_db_export.xml';
        }
        
        // Create and download blob
        const blob = await response.blob();
        downloadBlob(blob, filename);
        
        return true;
      } catch (error) {
        if (error.name === 'AbortError') {
          throw new Error('Export cancelled by user');
        }
        console.error('Export failed:', error);
        throw error;
      }
    })();
    
    return {
      promise,
      cancel: () => controller.abort()
    };
  }
};

export default {
  sourcesApi,
  photometryApi,
  redshiftApi,
  classificationApi,
  searchApi
}; 