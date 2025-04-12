import { useState, useEffect, useRef } from 'react';
import { QueryBuilder } from 'react-querybuilder';
import 'react-querybuilder/dist/query-builder.css';
import { searchApi, processSED, downloadSED } from '../services/api';
import ExportDialog from './ExportDialog';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';
import { LineChart } from 'lucide-react';

export default function QuerySearch() {
  const [query, setQuery] = useState({ combinator: 'and', rules: [] });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({ skip: 0, limit: 20, total: 0, sort_field: null, sort_direction: 'asc' });
  const [columnOrder, setColumnOrder] = useState([]);
  const [visibleColumns, setVisibleColumns] = useState({});
  const [showColumnSelector, setShowColumnSelector] = useState(false);
  const [showExportDialog, setShowExportDialog] = useState(false);
  const [queryRuntime, setQueryRuntime] = useState(0);
  const [queryTakingTooLong, setQueryTakingTooLong] = useState(false);
  const runtimeInterval = useRef(null);
  const searchRequestRef = useRef(null);
  const LONG_QUERY_THRESHOLD = 10000;
  const initialVisibilitySet = useRef(false);
  const [selectedSource, setSelectedSource] = useState(null);
  const [sedImage, setSedImage] = useState(null);
  const [sedLoading, setSedLoading] = useState(false);
  const [sedError, setSedError] = useState(null);
  const [showSedModal, setShowSedModal] = useState(false);
  const [selectedPhotometry, setSelectedPhotometry] = useState([]);
  const [selectedRows, setSelectedRows] = useState([]);
  const [sedInputMode, setSedInputMode] = useState('query');
  const [manualSourceName, setManualSourceName] = useState('');
  const [manualRedshift, setManualRedshift] = useState('');
  const [manualDataPoints, setManualDataPoints] = useState([]);
  const [showQueryModal, setShowQueryModal] = useState(false);
  const [pendingQuery, setPendingQuery] = useState(null);
  const [hasExecutedQuery, setHasExecutedQuery] = useState(false);
  const queryBuilderRef = useRef(null);

  const fields = [
    { name: 'agn_id', label: 'AGN ID', inputType: 'number' },
    { name: 'ra', label: 'Right Ascension', inputType: 'number' },
    { name: 'declination', label: 'Declination', inputType: 'number' },
    { name: 'band_label', label: 'Band Label' },
    { name: 'filter_name', label: 'Filter Name' },
    { name: 'mag_value', label: 'Magnitude Value', inputType: 'number' },
    { name: 'mag_error', label: 'Magnitude Error', inputType: 'number' },
    { name: 'extinction', label: 'Extinction', inputType: 'number' },
    { name: 'redshift_type', label: 'Redshift Type' },
    { name: 'z_value', label: 'Redshift Value', inputType: 'number' },
    { name: 'z_error', label: 'Redshift Error', inputType: 'number' },
    { name: 'spec_class', label: 'Spectroscopic Class' },
    { name: 'gen_class', label: 'General Class' },
    { name: 'xray_class', label: 'X-ray Class' },
    { name: 'best_class', label: 'Best Class' },
    { name: 'image_class', label: 'Image Class' },
    { name: 'sed_class', label: 'SED Class' }
  ];

  const fieldLabels = fields.reduce((acc, field) => {
    acc[field.name] = field.label;
    return acc;
  }, {});

  useEffect(() => {
    const allFieldNames = fields.map(field => field.name);

    const orderedColumns = getOrderedColumns(allFieldNames);
    setColumnOrder(orderedColumns);

    if (!initialVisibilitySet.current) {
      const initialVisibility = {};
      orderedColumns.forEach(field => {
        initialVisibility[field] = true;
      });
      setVisibleColumns(initialVisibility);
      initialVisibilitySet.current = true;
      console.log('Initial column visibility set:', initialVisibility);
    }
  }, [fields]);

  const getOrderedColumns = (columns) => {
    const preferredOrder = [
      'agn_id', 'ra', 'declination',
      'redshift_type', 'z_value', 'z_error',
      'spec_class', 'gen_class', 'xray_class', 'best_class', 'image_class', 'sed_class',
      'band_label', 'filter_name', 'mag_value', 'mag_error', 'extinction'
    ];
    return [...columns].sort((a, b) => {
      const indexA = preferredOrder.indexOf(a);
      const indexB = preferredOrder.indexOf(b);
      if (indexA >= 0 && indexB >= 0) return indexA - indexB;
      if (indexA >= 0) return -1;
      if (indexB >= 0) return 1;
      return a.localeCompare(b);
    });
  };

  const [lastExecutedQuery, setLastExecutedQuery] = useState(null);

  const executeSearch = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await searchApi.executeQuery(query, {
        skip: pagination.skip,
        limit: pagination.limit
      });
      
      setResults(response.items);
      setPagination(prev => ({
        ...prev,
        total: response.total
      }));
    } catch (err) {
      console.error('Search error:', err);
      setError(err.message || 'An error occurred during the search');
    } finally {
      setLoading(false);
    }
  };

  const getSortedResults = () => {
    if (!pagination.sort_field) return results;
    
    return [...results].sort((a, b) => {
      const aValue = a[pagination.sort_field];
      const bValue = b[pagination.sort_field];
      
      // Handle null/undefined values
      if (aValue == null) return pagination.sort_direction === 'asc' ? -1 : 1;
      if (bValue == null) return pagination.sort_direction === 'asc' ? 1 : -1;
      
      // Handle numeric values (including strings that can be converted to numbers)
      const aNum = Number(aValue);
      const bNum = Number(bValue);
      if (!isNaN(aNum) && !isNaN(bNum)) {
        return pagination.sort_direction === 'asc' ? aNum - bNum : bNum - aNum;
      }
      
      // Handle string values with case-insensitive comparison
      const aStr = String(aValue).toLowerCase();
      const bStr = String(bValue).toLowerCase();
      const comparison = aStr.localeCompare(bStr);
      return pagination.sort_direction === 'asc' ? comparison : -comparison;
    });
  };

  const getPaginatedResults = () => {
    const start = pagination.skip;
    const end = start + pagination.limit;
    return getSortedResults().slice(start, end);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    console.log('handleSubmit - Current state:', {
      hasExecutedQuery,
      resultsLength: results.length,
      currentQuery: query
    });
    
    // If a query has been executed before and there are results, show the modal
    if (hasExecutedQuery && results.length > 0) {
      console.log('Showing modal - hasExecutedQuery:', hasExecutedQuery, 'results.length:', results.length);
      setPendingQuery(query);
      setShowQueryModal(true);
      return;
    }
    
    // If no previous query or no results, execute immediately
    console.log('Executing query immediately - hasExecutedQuery:', hasExecutedQuery);
    setLastExecutedQuery(query);
    setHasExecutedQuery(true);
    executeSearch();
  };

  const handleCombineQueries = () => {
    console.log('handleCombineQueries - Current state:', {
      hasExecutedQuery,
      lastExecutedQuery,
      pendingQuery,
      resultsLength: results.length
    });
    
    // Create a new combined query with proper structure
    const combinedQuery = {
      combinator: 'or',
      rules: [
        // First query's rules
        ...lastExecutedQuery.rules.map(rule => ({
          ...rule,
          valueSource: 'value'
        })),
        // Second query's rules
        ...pendingQuery.rules.map(rule => ({
          ...rule,
          valueSource: 'value'
        }))
      ]
    };
    
    console.log('Combined Query Structure:', combinedQuery);
    
    // Clear the current results before executing the combined query
    setResults([]);
    setQuery(combinedQuery);
    setLastExecutedQuery(combinedQuery);
    setPendingQuery(null);
    setShowQueryModal(false);
    setHasExecutedQuery(true);
    executeSearch();
  };

  const handleNewQuery = () => {
    console.log('handleNewQuery - Current state:', {
      hasExecutedQuery,
      pendingQuery
    });
    
    // Clear everything first
    handleClear();
    
    // Use setTimeout to ensure state is reset before executing new query
    setTimeout(() => {
      setQuery(pendingQuery);
      setLastExecutedQuery(pendingQuery);
      setPendingQuery(null);
      setShowQueryModal(false);
      setHasExecutedQuery(true);
      executeSearch();
    }, 0);
  };

  const handleCancelModal = () => {
    console.log('handleCancelModal - Current state:', {
      hasExecutedQuery,
      pendingQuery
    });
    
    setPendingQuery(null);
    setShowQueryModal(false);
  };

  const getCurrentPage = () => Math.floor(pagination.skip / pagination.limit) + 1;
  const getTotalPages = () => Math.max(1, Math.ceil(pagination.total / pagination.limit));

  const handlePageChange = (newPage) => {
    if (newPage < 0) newPage = 0;
    const totalPages = getTotalPages();
    if (newPage >= totalPages) newPage = totalPages - 1;
    const newSkip = newPage * pagination.limit;
    if (newSkip !== pagination.skip) {
      setPagination({ ...pagination, skip: newSkip });
    }
  };

  const goToPage = (pageNum) => handlePageChange(pageNum - 1);
  const goToFirstPage = () => handlePageChange(0);
  const goToPreviousPage = () => handlePageChange(getCurrentPage() - 2);
  const goToNextPage = () => handlePageChange(getCurrentPage());
  const goToLastPage = () => handlePageChange(getTotalPages() - 1);

  const toggleColumnVisibility = (column) => {
    setVisibleColumns(prev => ({ ...prev, [column]: !prev[column] }));
  };

  const toggleAllColumns = (visible) => {
    const newVisibility = {};
    columnOrder.forEach(column => {
      newVisibility[column] = visible;
    });
    setVisibleColumns(newVisibility);
  };

  const handleSort = (field) => {
    if (pagination.sort_field === field) {
      // Toggle direction if clicking the same field
      setPagination(prev => ({
        ...prev,
        sort_direction: prev.sort_direction === 'asc' ? 'desc' : 'asc'
      }));
    } else {
      // Set new field and default to ascending
      setPagination(prev => ({
        ...prev,
        sort_field: field,
        sort_direction: 'asc'
      }));
    }
  };

  const getSortIndicator = (field) => {
    if (pagination.sort_field === field) {
      return pagination.sort_direction === 'asc' ? '↑' : '↓';
    }
    return '';
  };

  useEffect(() => {
    if (lastExecutedQuery !== null) {
      const paginationSearch = async () => {
        setLoading(true);
        setError(null);
        try {
          const searchParams = { skip: pagination.skip, limit: pagination.limit, sort_field: pagination.sort_field, sort_direction: pagination.sort_direction };
          const response = await searchApi.executeQuery(lastExecutedQuery, searchParams);
          if (response && response.items) {
            setResults(response.items);
            setPagination({ ...pagination, total: response.total || 0 });
          } else {
            setResults([]);
          }
        } catch (err) {
          console.error('Pagination search failed:', err);
          setError(err.message || 'Failed to paginate results');
        } finally {
          setLoading(false);
        }
      };
      paginationSearch();
    }
  }, [pagination.skip, pagination.limit, pagination.sort_field, pagination.sort_direction, lastExecutedQuery]);

  const getVisibleColumns = () => {
    if (!columnOrder || columnOrder.length === 0) return [];
    const visible = columnOrder.filter(column => visibleColumns[column] === true);
    return visible.length === 0 && columnOrder.length > 0 ? columnOrder.slice(0, 3) : visible;
  };

  const openExportDialog = () => {
    if (results.length > 0 && lastExecutedQuery) {
      setShowExportDialog(true);
    } else {
      setError('Execute a search first before exporting results');
    }
  };

  const renderColumnHeader = (column) => {
    const label = fieldLabels[column] || column;
    return (
      <th
        key={column}
        className="px-4 py-2 bg-gray-200 cursor-pointer hover:bg-gray-300"
        onClick={() => handleSort(column)}
      >
        {label}{getSortIndicator(column)}
      </th>
    );
  };

  const handleCancelSearch = () => {
    if (searchRequestRef.current) {
      searchRequestRef.current.cancel();
      searchRequestRef.current = null;
    }
    clearInterval(runtimeInterval.current);
    setLoading(false);
    setQueryTakingTooLong(false);
    setError({ message: 'Search cancelled by user' });
  };

  const handleClear = () => {
    console.log('handleClear - Resetting state');
    // Reset all state in a specific order
    setResults([]);
    setSelectedRows([]);
    setError(null);
    setLastExecutedQuery(null);
    setSedImage(null);
    setSedError(null);
    setPagination({ skip: 0, limit: 20, total: 0 });
    
    // Reset the query builder to its initial state
    setQuery({ 
      combinator: 'and', 
      rules: [] 
    });
    
    // Reset any form fields or selections
    if (queryBuilderRef.current) {
      // Reset the query builder component
      queryBuilderRef.current.setQuery({ 
        combinator: 'and', 
        rules: [] 
      });
    }
    
    // Set hasExecutedQuery last to ensure other states are reset first
    setHasExecutedQuery(false);
  };

  const handleSedAnalysis = async (source) => {
    setSelectedSource(source);
    setShowSedModal(true);
    setSedLoading(true);
    setSedError(null);
    setSelectedPhotometry([]);
    setSedImage(null);
    try {
      // Get all photometry data points for the source
      const photometryData = source.photometry || [];
      if (photometryData.length === 0) {
        throw new Error('No photometry data available for this source');
      }
      // Sort photometry data by wavelength
      const sortedPhotometry = [...photometryData].sort((a, b) => a.wavelength - b.wavelength);
      setSelectedPhotometry(sortedPhotometry);
    } catch (err) {
      setSedError(err.message || 'Failed to load photometry data');
    } finally {
      setSedLoading(false);
    }
  };

  const handleRowSelection = (result, event) => {
    // Only handle row clicks, not checkbox clicks
    if (event.target.type === 'checkbox') {
      return;
    }
    
    setSelectedRows(prev => {
      const isSelected = prev.some(r => r.agn_id === result.agn_id);
      if (isSelected) {
        return prev.filter(r => r.agn_id !== result.agn_id);
      } else {
        return [...prev, result];
      }
    });
  };

  const handleCheckboxChange = (result) => {
    setSelectedRows(prev => {
      const isSelected = prev.some(r => r.agn_id === result.agn_id);
      if (isSelected) {
        return prev.filter(r => r.agn_id !== result.agn_id);
      } else {
        return [...prev, result];
      }
    });
  };

  const handleGenerateSed = async () => {
    if (selectedRows.length === 0) {
      setSedError('Please select at least one source');
      return;
    }

    setSedLoading(true);
    setSedError(null);

    try {
      console.log('Starting SED generation for selected rows:', selectedRows);
      
      // Group photometry data by AGN ID to avoid duplicates
      const agnData = {};
      selectedRows.forEach(row => {
        if (!agnData[row.agn_id]) {
          agnData[row.agn_id] = {
            agn_id: row.agn_id,
            photometry: []
          };
        }
        if (row.band_label && row.mag_value != null) {
          agnData[row.agn_id].photometry.push({
            band: row.band_label,
            mag: row.mag_value
          });
        }
      });

      // Process each AGN's photometry data
      const dataPoints = Object.values(agnData)
        .map(agn => {
          // Sort photometry by wavelength
          const sortedPhotometry = agn.photometry.sort((a, b) => {
            const wavelengthMap = {
              'U': 0.36, 'B': 0.44, 'V': 0.55, 'R': 0.64, 'I': 0.79,
              'J': 1.25, 'H': 1.65, 'K': 2.2
            };
            return wavelengthMap[a.band] - wavelengthMap[b.band];
          });

          // Convert to wavelength,flux pairs
          return sortedPhotometry.map(phot => {
            const wavelengthMap = {
              'U': 0.36, 'B': 0.44, 'V': 0.55, 'R': 0.64, 'I': 0.79,
              'J': 1.25, 'H': 1.65, 'K': 2.2
            };
            
            const wavelengthMicrons = wavelengthMap[phot.band] || 0;
            // Convert wavelength from microns to Angstroms (1 micron = 10000 Angstroms)
            const wavelengthAngstroms = wavelengthMicrons * 10000;
            // Convert magnitude to flux
            const flux = Math.pow(10, -0.4 * phot.mag);
            
            console.log(`Processing AGN ${agn.agn_id}: band=${phot.band}, mag=${phot.mag}, wavelength=${wavelengthAngstroms}Å, flux=${flux}`);
            
            return `${wavelengthAngstroms},${flux}`;
          }).join(' ');
        })
        .join(' ');

      console.log('Final data points:', dataPoints);

      if (!dataPoints) {
        throw new Error('No valid data points to generate SED');
      }

      console.log('Sending data to SED processor...');
      const response = await processSED({ raw_data: dataPoints });
      console.log('SED processor response:', response);
      
      if (!response?.sed_name) {
        throw new Error('Invalid response from SED processing service');
      }

      const imageUrl = `${import.meta.env.VITE_API_URL}/queries/sed/sed/download/${response.sed_name}`;
      console.log('Generated SED image URL:', imageUrl);
      setSedImage(imageUrl);
    } catch (err) {
      console.error('Error generating SED:', err);
      setSedError(err.message || 'Failed to generate SED');
    } finally {
      setSedLoading(false);
    }
  };

  const togglePhotometrySelection = (photometry) => {
    setSelectedPhotometry(prev => {
      const isSelected = prev.some(p => p.phot_id === photometry.phot_id);
      if (isSelected) {
        return prev.filter(p => p.phot_id !== photometry.phot_id);
      } else {
        return [...prev, photometry];
      }
    });
  };

  const handleDownloadSed = async (imageUrl) => {
    try {
      const sedName = imageUrl.split('/').pop();
      const response = await downloadSED(sedName);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `sed_${sedName}.png`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading SED:', error);
      setSedError('Failed to download SED image');
    }
  };

  const handleGenerateManualSed = async () => {
    if (manualDataPoints.length === 0 || !manualSourceName) {
      setSedError('Please provide both source name and data points');
      return;
    }

    setSedLoading(true);
    setSedError(null);

    try {
      console.log('Starting manual SED generation');
      
      // Convert manual data points to the required format
      const dataPoints = manualDataPoints.map(point => `${point.wavelength},${point.flux},${point.error}`).join(' ');

      console.log('Sending data to SED processor...');
      const response = await processSED({ raw_data: dataPoints });
      console.log('SED processor response:', response);
      
      if (!response?.sed_name) {
        throw new Error('Invalid response from SED processing service');
      }

      const imageUrl = `${import.meta.env.VITE_API_URL}/queries/sed/sed/download/${response.sed_name}`;
      console.log('Generated SED image URL:', imageUrl);
      setSedImage(imageUrl);
    } catch (err) {
      console.error('Error generating manual SED:', err);
      setSedError(err.message || 'Failed to generate manual SED');
    } finally {
      setSedLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {showQueryModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl max-w-md w-full">
            <h3 className="text-lg font-semibold mb-4">Existing Query Results</h3>
            <p className="text-gray-600 mb-6">
              You have existing query results. Would you like to:
            </p>
            <div className="flex flex-col space-y-3">
              <button
                onClick={handleNewQuery}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Clear and Execute New Query
              </button>
              <button
                onClick={handleCombineQueries}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                Combine with Existing Query
              </button>
              <button
                onClick={handleCancelModal}
                className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Query Builder</h2>
        <form onSubmit={handleSubmit}>
          <QueryBuilder fields={fields} query={query} onQueryChange={setQuery} controlClassnames={{ queryBuilder: 'border p-4' }} ref={queryBuilderRef} />
          <div className="mt-4 flex justify-end space-x-2">
            {loading ? (
              <div className="flex space-x-3">
                <button type="button" onClick={handleCancelSearch} className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">Cancel</button>
                <div className="flex items-center space-x-2 bg-blue-50 px-4 py-2 rounded">
                  <LoadingSpinner size="sm" />
                  <span>{queryTakingTooLong ? `Still searching (${Math.floor(queryRuntime / 1000)}s)...` : 'Searching...'}</span>
                </div>
              </div>
            ) : (
              <div className="flex space-x-2">
                {results.length > 0 && (
                  <button 
                    type="button" 
                    onClick={handleClear} 
                    className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
                  >
                    Clear Results
                  </button>
                )}
                <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Execute Query</button>
              </div>
            )}
          </div>
        </form>
      </div>

      {queryTakingTooLong && !error && (
        <div className="bg-yellow-50 border border-yellow-400 text-yellow-800 px-4 py-3 rounded">
          <p className="font-medium">This query is taking longer than expected.</p>
          <p className="text-sm">Try simplifying or narrowing your query criteria.</p>
        </div>
      )}

      {error && <ErrorMessage error={error} />}

      {!loading && results.length === 0 && !error && lastExecutedQuery && (
        <div className="bg-blue-50 border border-blue-200 text-blue-800 px-4 py-3 rounded">
          No results found. Try adjusting your query criteria.
        </div>
      )}

      {results.length > 0 && (
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <div className="flex justify-between items-center p-4 border-b">
            <div className="flex items-center space-x-4">
              <div className="text-lg font-medium">Results ({pagination.total})</div>
              <div className="flex items-center space-x-2 bg-blue-50 px-3 py-1 rounded">
                <input
                  type="checkbox"
                  checked={results.length > 0 && selectedRows.length === results.length}
                  onChange={() => {
                    if (selectedRows.length === results.length) {
                      setSelectedRows([]);
                    } else {
                      setSelectedRows([...results]);
                    }
                  }}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
                />
                <span className="text-blue-800 font-medium">Select All Results</span>
                {selectedRows.length > 0 && (
                  <span className="text-blue-600 text-sm">
                    ({selectedRows.length} selected)
                  </span>
                )}
              </div>
            </div>
            <div className="flex space-x-2">
              <button onClick={() => setShowColumnSelector(!showColumnSelector)} className="px-3 py-1 bg-blue-100 text-blue-800 rounded hover:bg-blue-200">Columns</button>
              <button onClick={openExportDialog} className="px-3 py-1 bg-green-100 text-green-800 rounded hover:bg-green-200">Export</button>
            </div>
          </div>

          {showColumnSelector && (
            <div className="p-4 bg-gray-50 border-b">
              <div className="flex justify-between mb-2">
                <div className="font-medium">Select columns to display:</div>
                <div className="space-x-2">
                  <button onClick={() => toggleAllColumns(true)} className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded" type="button">Show all</button>
                  <button onClick={() => toggleAllColumns(false)} className="text-xs px-2 py-1 bg-red-100 text-red-800 rounded" type="button">Hide all</button>
                </div>
              </div>
              <div className="grid grid-cols-4 gap-2">
                {columnOrder.map(column => (
                  <div key={`col-select-${column}`} className="flex items-center">
                    <input
                      id={`col-checkbox-${column}`}
                      type="checkbox"
                      checked={!!visibleColumns[column]}
                      onChange={() => toggleColumnVisibility(column)}
                      className="mr-2"
                    />
                    <label htmlFor={`col-checkbox-${column}`} className="cursor-pointer text-sm">{fieldLabels[column] || column}</label>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    <div className="flex items-center space-x-2 bg-blue-50 p-2 rounded">
                      <input
                        type="checkbox"
                        checked={results.length > 0 && selectedRows.length === results.length}
                        onChange={() => {
                          if (selectedRows.length === results.length) {
                            setSelectedRows([]);
                          } else {
                            setSelectedRows([...results]);
                          }
                        }}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
                      />
                      <span className="text-blue-800">Select All</span>
                    </div>
                  </th>
                  {getVisibleColumns().map(column => (
                    <th key={column} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {renderColumnHeader(column)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {results.map((result, index) => {
                  const isSelected = selectedRows.some(r => r.agn_id === result.agn_id);
                  return (
                    <tr 
                      key={index} 
                      className={`hover:bg-gray-50 cursor-pointer transition-colors duration-150 ${
                        isSelected ? 'bg-blue-50 hover:bg-blue-100' : ''
                      }`}
                      onClick={(e) => handleRowSelection(result, e)}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => handleCheckboxChange(result)}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
                          onClick={(e) => e.stopPropagation()}
                        />
                      </td>
                      {getVisibleColumns().map(column => (
                        <td key={column} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {result[column]}
                        </td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          
          {/* Pagination Controls */}
          <div className="px-4 py-3 flex items-center justify-between border-t border-gray-200">
            <div className="flex-1 flex justify-between items-center">
              <div>
                <p className="text-sm text-gray-700">
                  Showing{' '}
                  <span className="font-medium">{pagination.skip + 1}</span>
                  {' '}-{' '}
                  <span className="font-medium">{Math.min(pagination.skip + pagination.limit, pagination.total)}</span>
                  {' '}of{' '}
                  <span className="font-medium">{pagination.total}</span>
                  {' '}results
                </p>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={goToFirstPage}
                  disabled={getCurrentPage() === 1}
                  className={`px-3 py-1 rounded ${
                    getCurrentPage() === 1
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                  }`}
                >
                  First
                </button>
                <button
                  onClick={goToPreviousPage}
                  disabled={getCurrentPage() === 1}
                  className={`px-3 py-1 rounded ${
                    getCurrentPage() === 1
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                  }`}
                >
                  Previous
                </button>
                <span className="px-3 py-1">
                  Page {getCurrentPage()} of {getTotalPages()}
                </span>
                <button
                  onClick={goToNextPage}
                  disabled={getCurrentPage() === getTotalPages()}
                  className={`px-3 py-1 rounded ${
                    getCurrentPage() === getTotalPages()
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                  }`}
                >
                  Next
                </button>
                <button
                  onClick={goToLastPage}
                  disabled={getCurrentPage() === getTotalPages()}
                  className={`px-3 py-1 rounded ${
                    getCurrentPage() === getTotalPages()
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                  }`}
                >
                  Last
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* SED Analysis Section */}
      <div className="mt-8 bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">SED Analysis</h2>
        
        <div className="mb-4">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setSedInputMode('query')}
                className={`${
                  sedInputMode === 'query'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Query Results
              </button>
              <button
                onClick={() => setSedInputMode('manual')}
                className={`${
                  sedInputMode === 'manual'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Manual Input
              </button>
            </nav>
          </div>
        </div>

        {sedInputMode === 'query' ? (
          <div>
            <div className="mb-4">
              <span className="text-sm text-gray-600">
                {selectedRows.length} source{selectedRows.length !== 1 ? 's' : ''} selected
              </span>
            </div>
            <button
              onClick={handleGenerateSed}
              disabled={selectedRows.length === 0}
              className={`px-4 py-2 rounded ${
                selectedRows.length === 0
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              Generate SED
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="grid grid-cols-1 gap-4">
              <div className="flex flex-col space-y-2">
                <label className="text-sm font-medium text-gray-700">Source Name</label>
                <input
                  type="text"
                  value={manualSourceName}
                  onChange={(e) => setManualSourceName(e.target.value)}
                  placeholder="Enter source name"
                  className="border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="flex flex-col space-y-2">
                <label className="text-sm font-medium text-gray-700">Redshift (z)</label>
                <input
                  type="number"
                  value={manualRedshift}
                  onChange={(e) => setManualRedshift(e.target.value)}
                  placeholder="Enter redshift value"
                  className="border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium">Data Points</h3>
                <button
                  onClick={() => setManualDataPoints([...manualDataPoints, { wavelength: '', flux: '', error: '' }])}
                  className="px-3 py-1 bg-green-100 text-green-800 rounded hover:bg-green-200 text-sm"
                >
                  Add Point
                </button>
              </div>
              
              <div className="space-y-2">
                {manualDataPoints.map((point, index) => (
                  <div key={index} className="grid grid-cols-3 gap-4 items-center">
                    <div>
                      <label className="text-sm text-gray-600">Wavelength (Å)</label>
                      <input
                        type="number"
                        value={point.wavelength}
                        onChange={(e) => {
                          const newPoints = [...manualDataPoints];
                          newPoints[index].wavelength = e.target.value;
                          setManualDataPoints(newPoints);
                        }}
                        className="border rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="text-sm text-gray-600">Flux (erg/s/cm²/Å)</label>
                      <input
                        type="number"
                        value={point.flux}
                        onChange={(e) => {
                          const newPoints = [...manualDataPoints];
                          newPoints[index].flux = e.target.value;
                          setManualDataPoints(newPoints);
                        }}
                        className="border rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="text-sm text-gray-600">Error</label>
                      <div className="flex space-x-2">
                        <input
                          type="number"
                          value={point.error}
                          onChange={(e) => {
                            const newPoints = [...manualDataPoints];
                            newPoints[index].error = e.target.value;
                            setManualDataPoints(newPoints);
                          }}
                          className="border rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <button
                          onClick={() => {
                            const newPoints = manualDataPoints.filter((_, i) => i !== index);
                            setManualDataPoints(newPoints);
                          }}
                          className="px-2 py-2 text-red-600 hover:text-red-800"
                        >
                          ×
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={handleGenerateManualSed}
              disabled={manualDataPoints.length === 0 || !manualSourceName}
              className={`px-4 py-2 rounded ${
                manualDataPoints.length === 0 || !manualSourceName
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              Generate SED
            </button>
          </div>
        )}

        {sedImage && (
          <div className="mt-6">
            <img src={sedImage} alt="SED Plot" className="max-w-full" />
            <div className="mt-4">
              <button
                onClick={handleDownloadSed}
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                Download SED
              </button>
            </div>
          </div>
        )}
      </div>

      <ExportDialog
        isOpen={showExportDialog}
        query={lastExecutedQuery}
        onClose={() => setShowExportDialog(false)}
        sortField={pagination.sort_field}
        sortDirection={pagination.sort_direction}
        visibleColumns={visibleColumns}
      />
    </div>
  );
}