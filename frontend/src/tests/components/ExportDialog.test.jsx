import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ExportDialog from '../../components/ExportDialog';
import { searchApi } from '../../services/api';

// Mock the API module
jest.mock('../../services/api', () => ({
  searchApi: {
    getAvailableFields: jest.fn(),
    exportResults: jest.fn(),
  },
}));

describe('ExportDialog Component', () => {
  const mockProps = {
    isOpen: true,
    onClose: jest.fn(),
    query: { combinator: 'and', rules: [] },
    visibleColumns: {
      'agn_id': true,
      'ra': true,
      'declination': false,
      'z_value': true,
    },
  };

  const mockAvailableFields = {
    categories: {
      source: ['agn_id', 'ra', 'declination'],
      redshift: ['z_value', 'z_error', 'redshift_type'],
    },
    all_fields: ['agn_id', 'ra', 'declination', 'z_value', 'z_error', 'redshift_type'],
  };

  beforeEach(() => {
    jest.clearAllMocks();
    searchApi.getAvailableFields.mockResolvedValue(mockAvailableFields);
    searchApi.exportResults.mockResolvedValue(true);
  });

  test('renders correctly when open', () => {
    render(<ExportDialog {...mockProps} />);
    
    expect(screen.getByText('Export Data')).toBeInTheDocument();
    expect(screen.getByText('Export Format')).toBeInTheDocument();
    expect(screen.getByText('CSV (Comma Separated Values)')).toBeInTheDocument();
    expect(screen.getByText('VOTable (Virtual Observatory Table)')).toBeInTheDocument();
  });

  test('does not render when closed', () => {
    render(<ExportDialog {...mockProps} isOpen={false} />);
    
    expect(screen.queryByText('Export Data')).not.toBeInTheDocument();
  });

  test('fetches available fields when opened', async () => {
    render(<ExportDialog {...mockProps} />);
    
    await waitFor(() => {
      expect(searchApi.getAvailableFields).toHaveBeenCalled();
    });
  });

  test('initializes selected fields from visible columns', async () => {
    render(<ExportDialog {...mockProps} />);
    
    // Wait for fields to be fetched
    await waitFor(() => {
      expect(searchApi.getAvailableFields).toHaveBeenCalled();
    });
    
    // Mock field checkboxes should reflect visibleColumns
    const agnIdCheckbox = screen.getByLabelText('agn_id');
    const raCheckbox = screen.getByLabelText('ra');
    const declinationCheckbox = screen.getByLabelText('declination');
    const zValueCheckbox = screen.getByLabelText('z_value');
    
    expect(agnIdCheckbox).toBeChecked();
    expect(raCheckbox).toBeChecked();
    expect(declinationCheckbox).not.toBeChecked();
    expect(zValueCheckbox).toBeChecked();
  });

  test('toggles field selection', async () => {
    render(<ExportDialog {...mockProps} />);
    
    // Wait for fields to be fetched
    await waitFor(() => {
      expect(searchApi.getAvailableFields).toHaveBeenCalled();
    });
    
    // Toggle a field
    const declinationCheckbox = screen.getByLabelText('declination');
    fireEvent.click(declinationCheckbox);
    
    // Check that the field is now selected
    expect(declinationCheckbox).toBeChecked();
    
    // Toggle it back
    fireEvent.click(declinationCheckbox);
    
    // Check that the field is now unselected
    expect(declinationCheckbox).not.toBeChecked();
  });

  test('toggles all fields with select/deselect all button', async () => {
    render(<ExportDialog {...mockProps} />);
    
    // Wait for fields to be fetched
    await waitFor(() => {
      expect(searchApi.getAvailableFields).toHaveBeenCalled();
    });
    
    // Click the "Select All" button
    const selectAllButton = screen.getByText('Select All');
    fireEvent.click(selectAllButton);
    
    // All checkboxes should be checked
    const checkboxes = screen.getAllByRole('checkbox').filter(cb => 
      cb.getAttribute('name') !== 'format' && 
      !cb.getAttribute('name')?.includes('category')
    );
    
    checkboxes.forEach(checkbox => {
      expect(checkbox).toBeChecked();
    });
    
    // Now the button should say "Deselect All"
    const deselectAllButton = screen.getByText('Deselect All');
    fireEvent.click(deselectAllButton);
    
    // All checkboxes should be unchecked
    checkboxes.forEach(checkbox => {
      expect(checkbox).not.toBeChecked();
    });
  });

  test('toggles category selection', async () => {
    render(<ExportDialog {...mockProps} />);
    
    // Wait for fields to be fetched
    await waitFor(() => {
      expect(searchApi.getAvailableFields).toHaveBeenCalled();
    });
    
    // Find source category checkbox
    const sourceCategoryCheckbox = screen.getAllByRole('checkbox')
      .find(cb => cb.closest('div')?.textContent?.includes('source'));
    
    // Click to select all in the category
    fireEvent.click(sourceCategoryCheckbox);
    
    // All source fields should be checked
    const sourceFields = ['agn_id', 'ra', 'declination'];
    sourceFields.forEach(field => {
      expect(screen.getByLabelText(field)).toBeChecked();
    });
    
    // Click again to deselect all in the category
    fireEvent.click(sourceCategoryCheckbox);
    
    // All source fields should be unchecked
    sourceFields.forEach(field => {
      expect(screen.getByLabelText(field)).not.toBeChecked();
    });
  });

  test('toggles metadata inclusion', async () => {
    render(<ExportDialog {...mockProps} />);
    
    // Wait for fields to be fetched
    await waitFor(() => {
      expect(searchApi.getAvailableFields).toHaveBeenCalled();
    });
    
    // Find metadata checkbox
    const metadataCheckbox = screen.getByLabelText(/include metadata/i);
    
    // Should be checked by default
    expect(metadataCheckbox).toBeChecked();
    
    // Toggle it
    fireEvent.click(metadataCheckbox);
    
    // Should be unchecked now
    expect(metadataCheckbox).not.toBeChecked();
  });

  test('calls exportResults with correct parameters when export button is clicked', async () => {
    render(<ExportDialog {...mockProps} />);
    
    // Wait for fields to be fetched
    await waitFor(() => {
      expect(searchApi.getAvailableFields).toHaveBeenCalled();
    });
    
    // Change format to VOTable
    const voTableRadio = screen.getByLabelText('VOTable (Virtual Observatory Table)');
    fireEvent.click(voTableRadio);
    
    // Click export button
    const exportButton = screen.getByText('Export');
    fireEvent.click(exportButton);
    
    // Check that exportResults was called with the correct parameters
    await waitFor(() => {
      expect(searchApi.exportResults).toHaveBeenCalledWith(
        mockProps.query,
        {
          format: 'votable',
          selected_fields: ['agn_id', 'ra', 'z_value'], // The initially checked fields
          include_metadata: true,
        }
      );
    });
    
    // Check that onClose was called
    expect(mockProps.onClose).toHaveBeenCalled();
  });

  test('shows error message when export fails', async () => {
    // Setup export to fail
    searchApi.exportResults.mockRejectedValue(new Error('Export failed'));
    
    render(<ExportDialog {...mockProps} />);
    
    // Wait for fields to be fetched
    await waitFor(() => {
      expect(searchApi.getAvailableFields).toHaveBeenCalled();
    });
    
    // Click export button
    const exportButton = screen.getByText('Export');
    fireEvent.click(exportButton);
    
    // Check that error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Export failed. Please try again.')).toBeInTheDocument();
    });
    
    // Check that onClose was not called
    expect(mockProps.onClose).not.toHaveBeenCalled();
  });

  test('shows error message when fetching fields fails', async () => {
    // Setup getAvailableFields to fail
    searchApi.getAvailableFields.mockRejectedValue(new Error('Failed to fetch fields'));
    
    render(<ExportDialog {...mockProps} />);
    
    // Check that error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Failed to load available fields. Please try again.')).toBeInTheDocument();
    });
  });

  test('disable export button when no fields selected', async () => {
    render(<ExportDialog {...mockProps} />);
    
    // Wait for fields to be fetched
    await waitFor(() => {
      expect(searchApi.getAvailableFields).toHaveBeenCalled();
    });
    
    // Deselect all fields
    const deselectAllButton = screen.getByText('Select All'); // Initially it's "Select All" since not all fields are selected
    fireEvent.click(deselectAllButton); // This selects all fields
    
    const nowDeselectAllButton = screen.getByText('Deselect All');
    fireEvent.click(nowDeselectAllButton); // This deselects all fields
    
    // Export button should be disabled
    const exportButton = screen.getByText('Export');
    expect(exportButton).toBeDisabled();
  });
}); 