import { searchApi } from '../../services/api';

// Mock global fetch
global.fetch = jest.fn();

// Mock URL functions
global.URL.createObjectURL = jest.fn(() => 'mock-url');
global.URL.revokeObjectURL = jest.fn();

// Mock DOM elements
document.body.appendChild = jest.fn();
document.body.removeChild = jest.fn();

describe('API Service - Export Functions', () => {
  const API_BASE_URL = 'http://localhost:8000/api/v1';
  
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Create a mock element to simulate the download link
    const mockLink = {
      href: '',
      setAttribute: jest.fn(),
      click: jest.fn(),
      remove: jest.fn()
    };
    
    // Mock document.createElement to return our mock link
    document.createElement = jest.fn(() => mockLink);
  });
  
  describe('exportResults', () => {
    const mockQuery = { combinator: 'and', rules: [] };
    const mockOptions = {
      format: 'csv',
      selected_fields: ['agn_id', 'ra', 'declination'],
      include_metadata: true
    };
    
    it('calls fetch with the correct parameters', async () => {
      // Setup mock response
      const mockResponse = {
        ok: true,
        headers: new Headers({
          'content-disposition': 'attachment; filename=agn_db_export.csv'
        }),
        blob: jest.fn().mockResolvedValue('mock-blob')
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function
      await searchApi.exportResults(mockQuery, mockOptions);
      
      // Check fetch was called with correct arguments
      expect(fetch).toHaveBeenCalledWith(`${API_BASE_URL}/search/export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: mockQuery,
          export_options: mockOptions
        })
      });
    });
    
    it('extracts filename from content-disposition header', async () => {
      // Setup mock response
      const mockResponse = {
        ok: true,
        headers: new Headers({
          'content-disposition': 'attachment; filename=custom_filename.csv'
        }),
        blob: jest.fn().mockResolvedValue('mock-blob')
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function
      await searchApi.exportResults(mockQuery, mockOptions);
      
      // Get the mock link element
      const mockLink = document.createElement();
      
      // Check filename was extracted correctly
      expect(mockLink.setAttribute).toHaveBeenCalledWith('download', 'custom_filename.csv');
    });
    
    it('uses default filename when content-disposition is not present', async () => {
      // Setup mock response
      const mockResponse = {
        ok: true,
        headers: new Headers({}),
        blob: jest.fn().mockResolvedValue('mock-blob')
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function
      await searchApi.exportResults(mockQuery, mockOptions);
      
      // Get the mock link element
      const mockLink = document.createElement();
      
      // Check default filename was used
      expect(mockLink.setAttribute).toHaveBeenCalledWith('download', 'export.csv');
    });
    
    it('uses votable extension for votable format', async () => {
      // Setup mock response
      const mockResponse = {
        ok: true,
        headers: new Headers({}),
        blob: jest.fn().mockResolvedValue('mock-blob')
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function with votable format
      await searchApi.exportResults(mockQuery, { ...mockOptions, format: 'votable' });
      
      // Get the mock link element
      const mockLink = document.createElement();
      
      // Check filename with xml extension was used
      expect(mockLink.setAttribute).toHaveBeenCalledWith('download', 'agn_db_export.xml');
    });
    
    it('initiates download by creating and clicking a link', async () => {
      // Setup mock response
      const mockResponse = {
        ok: true,
        headers: new Headers({}),
        blob: jest.fn().mockResolvedValue('mock-blob')
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function
      await searchApi.exportResults(mockQuery, mockOptions);
      
      // Get the mock link element
      const mockLink = document.createElement();
      
      // Check URL was created
      expect(URL.createObjectURL).toHaveBeenCalledWith('mock-blob');
      
      // Check link was appended, clicked, and removed
      expect(document.body.appendChild).toHaveBeenCalled();
      expect(mockLink.click).toHaveBeenCalled();
      expect(mockLink.remove).toHaveBeenCalled();
      
      // Check URL was revoked
      expect(URL.revokeObjectURL).toHaveBeenCalledWith('mock-url');
    });
    
    it('throws an error when fetch fails', async () => {
      // Setup error response
      const mockResponse = {
        ok: false,
        text: jest.fn().mockResolvedValue('Server error')
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function and expect it to throw
      await expect(searchApi.exportResults(mockQuery, mockOptions)).rejects.toThrow('Server error');
    });
    
    it('throws an error when fetch rejects', async () => {
      // Setup network error
      fetch.mockRejectedValue(new Error('Network error'));
      
      // Call the function and expect it to throw
      await expect(searchApi.exportResults(mockQuery, mockOptions)).rejects.toThrow('Network error');
    });
  });
  
  describe('getAvailableFields', () => {
    it('calls the correct endpoint', async () => {
      // Setup mock response
      const mockResponse = {
        ok: true,
        headers: new Headers({
          'content-type': 'application/json'
        }),
        json: jest.fn().mockResolvedValue({
          categories: {
            source: ['agn_id', 'ra', 'declination']
          },
          all_fields: ['agn_id', 'ra', 'declination']
        })
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function
      await searchApi.getAvailableFields();
      
      // Check fetch was called with correct URL
      expect(fetch).toHaveBeenCalledWith(`${API_BASE_URL}/search/available-fields`, expect.any(Object));
    });
  });
}); 