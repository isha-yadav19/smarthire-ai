"""
Test PDF Parsing Success Rate
"""

from parsers.resume_parser import ResumeParser
from pathlib import Path

def test_pdf_parsing():
    parser = ResumeParser()
    input_dir = Path('input')
    
    # Get first 10 PDF files
    pdf_files = list(input_dir.glob('REAL_*.pdf'))[:10]
    
    print(f"Testing {len(pdf_files)} PDF files...")
    print("=" * 60)
    
    success = 0
    failed = 0
    results = []
    
    for pdf_file in pdf_files:
        try:
            result = parser.parse_file(str(pdf_file))
            text_length = len(result['text'])
            
            if text_length > 100:  # At least 100 characters
                success += 1
                status = "[OK]"
                results.append({
                    'file': pdf_file.name,
                    'status': 'success',
                    'length': text_length
                })
            else:
                failed += 1
                status = "[FAIL]"
                results.append({
                    'file': pdf_file.name,
                    'status': 'failed',
                    'length': text_length
                })
            
            print(f"{status} - {pdf_file.name} ({text_length} chars)")
            
        except Exception as e:
            failed += 1
            status = "[ERROR]"
            results.append({
                'file': pdf_file.name,
                'status': 'error',
                'error': str(e)
            })
            print(f"{status} - {pdf_file.name}: {e}")
    
    print("=" * 60)
    print(f"\nResults:")
    print(f"  Success: {success}/{len(pdf_files)} ({success/len(pdf_files)*100:.1f}%)")
    print(f"  Failed:  {failed}/{len(pdf_files)}")
    
    if success >= 8:
        print("\n[VERDICT] PDF parsing is RELIABLE - KEEP IT")
    elif success >= 5:
        print("\n[VERDICT] PDF parsing is OK - ADD TEXT FALLBACK")
    else:
        print("\n[VERDICT] PDF parsing is UNRELIABLE - CONSIDER REMOVING")
    
    return results

if __name__ == "__main__":
    test_pdf_parsing()
