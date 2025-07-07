import pytest
import tempfile
import os
from csv_processor import CSVProcessor, parse_filter_condition, parse_aggregate_condition


class TestCSVProcessor:
    """Test cases for CSVProcessor class."""

    def setup_method(self):
        """Setup test data before each test method."""
        # Create temporary CSV file for testing
        self.test_data = [
            "name,brand,price,rating\n",
            "iphone 15 pro,apple,999,4.9\n",
            "galaxy s23 ultra,samsung,1199,4.8\n",
            "redmi note 12,xiaomi,199,4.6\n",
            "poco x5 pro,xiaomi,299,4.4\n"
        ]
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.temp_file.writelines(self.test_data)
        self.temp_file.close()
        
        self.processor = CSVProcessor(self.temp_file.name)
        self.processor.load_data()
    
    def teardown_method(self):
        """Cleanup after each test method."""
        os.unlink(self.temp_file.name)
    
    def test_load_data(self):
        """Test loading CSV data."""
        assert len(self.processor.data) == 4
        assert self.processor.headers == ['name', 'brand', 'price', 'rating']
        assert self.processor.data[0]['name'] == 'iphone 15 pro'
        assert self.processor.data[0]['brand'] == 'apple'
    
    def test_filter_numeric_greater_than(self):
        """Test filtering with numeric greater than operator."""
        result = self.processor.filter_data('price', '>', '500')
        assert len(result) == 2
        assert result[0]['name'] == 'iphone 15 pro'
        assert result[1]['name'] == 'galaxy s23 ultra'
    
    def test_filter_numeric_less_than(self):
        """Test filtering with numeric less than operator."""
        result = self.processor.filter_data('price', '<', '300')
        assert len(result) == 2
        assert result[0]['name'] == 'redmi note 12'
        assert result[1]['name'] == 'poco x5 pro'
    
    def test_filter_numeric_equal(self):
        """Test filtering with numeric equal operator."""
        result = self.processor.filter_data('price', '=', '999')
        assert len(result) == 1
        assert result[0]['name'] == 'iphone 15 pro'
    
    def test_filter_string_equal(self):
        """Test filtering with string equal operator."""
        result = self.processor.filter_data('brand', '=', 'xiaomi')
        assert len(result) == 2
        assert result[0]['name'] == 'redmi note 12'
        assert result[1]['name'] == 'poco x5 pro'
    
    def test_filter_string_comparison(self):
        """Test filtering with string comparison operators."""
        result = self.processor.filter_data('brand', '>', 'apple')
        assert len(result) == 3  # samsung, xiaomi, xiaomi
    
    def test_filter_nonexistent_column(self):
        """Test filtering with non-existent column."""
        with pytest.raises(SystemExit):
            self.processor.filter_data('nonexistent', '=', 'value')
    
    def test_aggregate_average(self):
        """Test aggregation with average operation."""
        result = self.processor.aggregate_data('price', 'avg')
        expected_avg = (999 + 1199 + 199 + 299) / 4
        assert result['operation'] == 'Average'
        assert result['column'] == 'price'
        assert result['value'] == expected_avg
    
    def test_aggregate_minimum(self):
        """Test aggregation with minimum operation."""
        result = self.processor.aggregate_data('price', 'min')
        assert result['operation'] == 'Minimum'
        assert result['column'] == 'price'
        assert result['value'] == 199
    
    def test_aggregate_maximum(self):
        """Test aggregation with maximum operation."""
        result = self.processor.aggregate_data('price', 'max')
        assert result['operation'] == 'Maximum'
        assert result['column'] == 'price'
        assert result['value'] == 1199
    
    def test_aggregate_nonexistent_column(self):
        """Test aggregation with non-existent column."""
        with pytest.raises(SystemExit):
            self.processor.aggregate_data('nonexistent', 'avg')
    
    def test_aggregate_invalid_operation(self):
        """Test aggregation with invalid operation."""
        with pytest.raises(SystemExit):
            self.processor.aggregate_data('price', 'invalid')
    
    def test_aggregate_non_numeric_column(self):
        """Test aggregation with non-numeric column."""
        with pytest.raises(SystemExit):
            self.processor.aggregate_data('brand', 'avg')


class TestParsingFunctions:
    """Test cases for parsing functions."""
    
    def test_parse_filter_condition_equal(self):
        """Test parsing filter condition with equal operator."""
        column, operator, value = parse_filter_condition('price=999')
        assert column == 'price'
        assert operator == '='
        assert value == '999'
    
    def test_parse_filter_condition_greater(self):
        """Test parsing filter condition with greater than operator."""
        column, operator, value = parse_filter_condition('price>500')
        assert column == 'price'
        assert operator == '>'
        assert value == '500'
    
    def test_parse_filter_condition_less(self):
        """Test parsing filter condition with less than operator."""
        column, operator, value = parse_filter_condition('rating<4.5')
        assert column == 'rating'
        assert operator == '<'
        assert value == '4.5'
    
    def test_parse_filter_condition_with_spaces(self):
        """Test parsing filter condition with spaces."""
        column, operator, value = parse_filter_condition('brand = apple')
        assert column == 'brand'
        assert operator == '='
        assert value == 'apple'
    
    def test_parse_filter_condition_invalid(self):
        """Test parsing invalid filter condition."""
        with pytest.raises(SystemExit):
            parse_filter_condition('invalid_condition')
    
    def test_parse_aggregate_condition_valid(self):
        """Test parsing valid aggregate condition."""
        column, operation = parse_aggregate_condition('price=avg')
        assert column == 'price'
        assert operation == 'avg'
    
    def test_parse_aggregate_condition_with_spaces(self):
        """Test parsing aggregate condition with spaces."""
        column, operation = parse_aggregate_condition('price = avg')
        assert column == 'price'
        assert operation == 'avg'
    
    def test_parse_aggregate_condition_invalid_format(self):
        """Test parsing invalid aggregate condition format."""
        with pytest.raises(SystemExit):
            parse_aggregate_condition('invalid_format')
    
    def test_parse_aggregate_condition_invalid_operation(self):
        """Test parsing aggregate condition with invalid operation."""
        with pytest.raises(SystemExit):
            parse_aggregate_condition('price=invalid')


class TestCSVProcessorFileHandling:
    """Test cases for file handling in CSVProcessor."""
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent file."""
        processor = CSVProcessor('nonexistent.csv')
        with pytest.raises(SystemExit):
            processor.load_data()
    
    def test_load_empty_file(self):
        """Test loading empty CSV file."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        temp_file.write("")
        temp_file.close()
        
        processor = CSVProcessor(temp_file.name)
        processor.load_data()
        
        assert len(processor.data) == 0
        assert processor.headers == []
        
        os.unlink(temp_file.name)
    
    def test_load_single_row_file(self):
        """Test loading CSV file with single row."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        temp_file.write("name,price\ntest,100\n")
        temp_file.close()
        
        processor = CSVProcessor(temp_file.name)
        processor.load_data()
        
        assert len(processor.data) == 1
        assert processor.headers == ['name', 'price']
        assert processor.data[0]['name'] == 'test'
        assert processor.data[0]['price'] == '100'
        
        os.unlink(temp_file.name)


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Setup test data with edge cases."""
        self.edge_case_data = [
            "name,category,price,available\n",
            "product1,electronics,0,true\n",
            "product2,books,-5.99,false\n",
            "product3,clothes,100.50,true\n",
        ]
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.temp_file.writelines(self.edge_case_data)
        self.temp_file.close()
        
        self.processor = CSVProcessor(self.temp_file.name)
        self.processor.load_data()
    
    def teardown_method(self):
        """Cleanup after each test method."""
        os.unlink(self.temp_file.name)
    
    def test_filter_zero_value(self):
        """Test filtering with zero value."""
        result = self.processor.filter_data('price', '=', '0')
        assert len(result) == 1
        assert result[0]['name'] == 'product1'
    
    def test_filter_negative_value(self):
        """Test filtering with negative value."""
        result = self.processor.filter_data('price', '<', '0')
        assert len(result) == 1
        assert result[0]['name'] == 'product2'
    
    def test_filter_decimal_value(self):
        """Test filtering with decimal value."""
        result = self.processor.filter_data('price', '>', '50.0')
        assert len(result) == 1
        assert result[0]['name'] == 'product3'
    
    def test_aggregate_with_negative_values(self):
        """Test aggregation with negative values."""
        result = self.processor.aggregate_data('price', 'min')
        assert result['value'] == -5.99
    
    def test_aggregate_with_zero_values(self):
        """Test aggregation with zero values."""
        result = self.processor.aggregate_data('price', 'avg')
        expected_avg = (0 + (-5.99) + 100.50) / 3
        assert abs(result['value'] - expected_avg) < 0.001
