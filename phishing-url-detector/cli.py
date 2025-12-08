#!/usr/bin/env python3
"""
Command-line interface for Phishing URL Detector (Windows Compatible)

Quick URL checking from the terminal.
"""

import sys
import argparse
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from detector import PhishingDetector
from utils.config_loader import get_config


def print_banner():
    """Print CLI banner."""
    banner = """
==============================================================
                                                           
         PHISHING URL DETECTOR - CLI TOOL             
                                                           
==============================================================
    """
    print(banner)


def print_result(result):
    """Print analysis result in formatted output."""
    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    
    # URL
    print(f"\nURL: {result['url']}")
    
    # Risk Level
    risk_level = result['risk_level']
    print(f"\nRisk Level: {risk_level}")
    
    # Scores
    print(f"Risk Score: {result['risk_score']:.2%}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    # Verdict
    if result['is_phishing']:
        print(f"\nVERDICT: PHISHING DETECTED")
    else:
        print(f"\nVERDICT: APPEARS SAFE")
    
    # Threat Intelligence
    if result.get('threat_intel_matches'):
        print(f"\nThreat Intelligence Matches:")
        for source in result['threat_intel_matches']:
            print(f"   - {source}")
    
    # Reasons
    if result.get('reasons'):
        print(f"\nDetection Reasons:")
        for i, reason in enumerate(result['reasons'], 1):
            print(f"   {i}. {reason}")
    
    print("\n" + "=" * 60)


def print_json_result(result):
    """Print result as JSON."""
    print(json.dumps(result, indent=2))


def check_url(url, network=True, json_output=False):
    """
    Check a URL for phishing.
    
    Args:
        url: URL to check
        network: Include network features
        json_output: Output as JSON
    """
    try:
        # Initialize detector
        detector = PhishingDetector()
        
        if not json_output:
            print(f"\nAnalyzing: {url}")
            print("Please wait...")
        
        # Analyze URL
        result = detector.analyze_url(url, include_network=network)
        
        # Print result
        if json_output:
            print_json_result(result)
        else:
            print_result(result)
        
        # Return exit code based on result
        return 1 if result['is_phishing'] else 0
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}", file=sys.stderr)
        return 2


def check_file(filepath, network=True, json_output=False):
    """
    Check multiple URLs from a file.
    
    Args:
        filepath: Path to file with URLs (one per line)
        network: Include network features
        json_output: Output as JSON
    """
    try:
        # Read URLs from file
        with open(filepath, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not urls:
            print("[ERROR] No URLs found in file", file=sys.stderr)
            return 2
        
        print(f"\nFound {len(urls)} URLs to analyze\n")
        
        # Initialize detector
        detector = PhishingDetector()
        
        # Analyze each URL
        results = []
        phishing_count = 0
        
        for i, url in enumerate(urls, 1):
            if not json_output:
                print(f"[{i}/{len(urls)}] Analyzing: {url}")
            
            result = detector.analyze_url(url, include_network=network)
            results.append(result)
            
            if result['is_phishing']:
                phishing_count += 1
            
            if not json_output:
                risk_level = result['risk_level']
                print(f"    -> Risk: {risk_level} ({result['risk_score']:.2%})\n")
        
        # Print summary
        if json_output:
            print(json.dumps({
                'total': len(results),
                'phishing_count': phishing_count,
                'results': results
            }, indent=2))
        else:
            print("\n" + "=" * 60)
            print("BATCH ANALYSIS SUMMARY")
            print("=" * 60)
            print(f"Total URLs: {len(results)}")
            print(f"Phishing Detected: {phishing_count}")
            print(f"Safe URLs: {len(results) - phishing_count}")
            print("=" * 60)
        
        return 1 if phishing_count > 0 else 0
        
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"[ERROR] {str(e)}", file=sys.stderr)
        return 2


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Phishing URL Detector - Command Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check a single URL
  python cli.py https://suspicious-site.com
  
  # Check URL without network features (faster)
  python cli.py --no-network https://example.com
  
  # Check multiple URLs from file
  python cli.py --file urls.txt
  
  # Output as JSON
  python cli.py --json https://example.com
        """
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        help='URL to analyze'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='File containing URLs (one per line)'
    )
    
    parser.add_argument(
        '--no-network',
        action='store_true',
        help='Disable network features (faster analysis)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Phishing URL Detector v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Print banner (unless JSON output)
    if not args.json:
        print_banner()
    
    # Validate arguments
    if not args.url and not args.file:
        parser.print_help()
        return 2
    
    # Check if file or single URL
    if args.file:
        exit_code = check_file(
            args.file,
            network=not args.no_network,
            json_output=args.json
        )
    else:
        exit_code = check_url(
            args.url,
            network=not args.no_network,
            json_output=args.json
        )
    
    return exit_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[WARNING] Analysis cancelled by user")
        sys.exit(130)
