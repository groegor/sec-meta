import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from secmeta.api import Submissions
from secmeta.cli import main, parse_args


class TestSubmissionsBasic:
    """Very basic tests that don't assume DataFrame structure"""
    
    def test_submissions_can_be_created(self):
        """Test that Submissions objects can be instantiated"""
        # These should not raise errors during instantiation
        sub1 = Submissions(cik="123", name="Test", email="test@example.com")
        sub2 = Submissions(ticker="AAPL", name="Test", email="test@example.com")
        sub3 = Submissions(cik="123", credentials="Test <test@example.com>")
        
        assert sub1 is not None
        assert sub2 is not None
        assert sub3 is not None
    
    @patch('secmeta.api.harvest')
    def test_to_dataframe_returns_dataframe(self, mock_harvest):
        """Test that to_dataframe returns some kind of DataFrame, regardless of structure"""
        # Mock harvest to return something, doesn't matter what
        mock_harvest.return_value = pd.DataFrame({'test': [1, 2, 3]})
        
        sub = Submissions(cik="123", name="Test", email="test@example.com")
        result = sub.to_dataframe()
        
        # Very basic check - just ensure it returns a DataFrame
        assert isinstance(result, pd.DataFrame)
        print(f"DEBUG: Returned DataFrame has columns: {list(result.columns)}")
        print(f"DEBUG: DataFrame shape: {result.shape}")
        print(f"DEBUG: DataFrame:\n{result}")
    
    @patch('secmeta.api.ids_to_ciks')
    def test_ticker_resolution_called(self, mock_ids_to_ciks):
        """Test that ticker resolution is attempted, don't check the result"""
        # Based on your code: ids_to_ciks([id_], "ticker", self.ua)[0]
        # It expects a list where [0] gives the CIK for the first ticker
        mock_ids_to_ciks.return_value = ["0000320193"]  # List with one CIK
        
        # Test that we can create the object
        sub = Submissions(ticker="AAPL", name="Test", email="test@example.com")
        
        # Verify that ids_to_ciks was called with the right parameters
        mock_ids_to_ciks.assert_called_once_with(["AAPL"], "ticker", "secmeta (Test <test@example.com>)")
        
        # Don't call to_dataframe() since we just want to test the initialization logic
        assert sub is not None
        print("DEBUG: Successfully created Submissions object with ticker")


class TestCLIArgParsing:
    """Test CLI argument parsing - these are very reliable"""
    
    def test_parse_args_basic_ticker(self):
        """Test basic ticker argument parsing"""
        args = parse_args(["AAPL", "-c", "Test <test@example.com>"])
        assert args.identifiers == ["AAPL"]
        assert args.type == "ticker"
        assert args.credentials == "Test <test@example.com>"
    
    def test_parse_args_multiple_tickers(self):
        """Test multiple ticker arguments"""
        args = parse_args(["AAPL", "GOOGL", "MSFT", "-c", "Test <test@example.com>"])
        assert args.identifiers == ["AAPL", "GOOGL", "MSFT"]
        assert args.type == "ticker"
    
    def test_parse_args_form_filter(self):
        """Test form filtering argument"""
        args = parse_args(["AAPL", "--form", "10-K", "-c", "Test <test@example.com>"])
        assert args.form == "10-K"
    
    def test_parse_args_year_range(self):
        """Test year range arguments"""
        args = parse_args([
            "AAPL", 
            "--year-from", "2020", 
            "--year-to", "2023", 
            "-c", "Test <test@example.com>"
        ])
        assert args.year_from == 2020
        assert args.year_to == 2023
    
    def test_parse_args_cik_type(self):
        """Test CIK type argument"""
        args = parse_args(["-t", "cik", "0001288776", "-c", "Test <test@example.com>"])
        assert args.identifiers == ["0001288776"]
        assert args.type == "cik"


class TestCLIBasic:
    """Very basic CLI tests"""
    
    @patch('secmeta.cli.Submissions')
    @patch('pandas.DataFrame.to_csv')
    def test_cli_runs_without_error(self, mock_to_csv, mock_submissions):
        """Test that CLI can run without crashing"""
        # Mock Submissions to return something
        mock_instance = MagicMock()
        mock_df = pd.DataFrame({'test': [1]})  # Simple DataFrame
        mock_instance.to_dataframe.return_value = mock_df
        mock_submissions.return_value = mock_instance
        
        # This should not raise an exception
        main(["AAPL", "-c", "Test <test@example.com>"])
        
        # Verify basic flow happened
        mock_submissions.assert_called_once()
        mock_to_csv.assert_called_once()
    
    def test_cli_error_no_identifiers(self):
        """Test CLI error when no identifiers provided"""
        with pytest.raises(SystemExit):
            main(["-c", "Test <test@example.com>"])
    
    def test_cli_error_no_credentials(self):
        """Test CLI error when no credentials provided"""
        with pytest.raises(SystemExit):
            main(["AAPL"])


class TestImports:
    """Test that imports work"""
    
    def test_imports_work(self):
        """Test that all modules can be imported"""
        from secmeta.api import Submissions
        from secmeta.cli import main, parse_args
        assert Submissions is not None
        assert main is not None
        assert parse_args is not None