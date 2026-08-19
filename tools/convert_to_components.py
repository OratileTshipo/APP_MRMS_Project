#!/usr/bin/env python3
"""
Convert container-based screens to component-based screens.
Replaces inline sidebar/header containers with CanvasComponent references.
"""
import re
import os
import sys

def find_sidebar_block(content, screen_prefix):
    """Find the sidebar container block and return its start/end positions."""
    # Find the sidebar start
    sidebar_patterns = [
        rf'(\s+- {screen_prefix}Sidebar_con:)',
        rf'(\s+- {screen_prefix}NavRail_con:)',
    ]
    
    for pattern in sidebar_patterns:
        match = re.search(pattern, content)
        if match:
            start = match.start()
            # Find the matching indentation level for the end
            # The sidebar ends when we find a sibling at the same indentation
            lines = content[start:].split('\n')
            indent_level = None
            end_offset = start
            
            for i, line in enumerate(lines[1:], 1):
                stripped = line.rstrip()
                if stripped and not stripped.startswith('#'):
                    current_indent = len(stripped) - len(stripped.lstrip())
                    if indent_level is None:
                        indent_level = current_indent
                    elif current_indent < indent_level:
                        # Found a sibling or parent - sidebar ends here
                        end_offset = start + len('\n'.join(lines[:i]))
                        break
            
            return start, end_offset
    return None, None

def find_header_block(content, screen_prefix):
    """Find the header container block and return its start/end positions."""
    header_patterns = [
        rf'(\s+- {screen_prefix}Header_con:)',
        rf'(\s+- {screen_prefix}AppHeader_con:)',
    ]
    
    for pattern in header_patterns:
        match = re.search(pattern, content)
        if match:
            start = match.start()
            # Find the matching indentation level for the end
            lines = content[start:].split('\n')
            indent_level = None
            end_offset = start
            
            for i, line in enumerate(lines[1:], 1):
                stripped = line.rstrip()
                if stripped and not stripped.startswith('#'):
                    current_indent = len(stripped) - len(stripped.lstrip())
                    if indent_level is None:
                        indent_level = current_indent
                    elif current_indent < indent_level:
                        # Found a sibling or parent - header ends here
                        end_offset = start + len('\n'.join(lines[:i]))
                        break
            
            return start, end_offset
    return None, None

def convert_screen_to_components(filepath, screen_name):
    """Convert a single screen file to use components."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine screen prefix from screen name
    # e.g., scr_Home -> Home, scr_Projects -> Projects
    screen_prefix = screen_name.replace('scr_', '')
    
    # Check if this screen already uses components
    if 'CanvasComponent' in content:
        print(f"  {screen_name}: Already uses components, skipping")
        return False
    
    # Find and replace sidebar
    sidebar_start, sidebar_end = find_sidebar_block(content, screen_prefix)
    if sidebar_start is not None:
        sidebar_block = content[sidebar_start:sidebar_end]
        # Determine the indentation
        first_line = sidebar_block.split('\n')[0]
        indent = len(first_line) - len(first_line.lstrip())
        indent_str = ' ' * indent
        
        # Create component reference
        component_ref = f"""{indent_str}- {screen_prefix}NavRail:
{indent_str}    Control: CanvasComponent
{indent_str}    ComponentName: cmp_NavRail
{indent_str}    Properties:
{indent_str}      ActiveScreen: =\"{screen_name}\""""
        
        content = content[:sidebar_start] + component_ref + content[sidebar_end:]
        print(f"  {screen_name}: Replaced sidebar with cmp_NavRail")
    
    # Find and replace header
    header_start, header_end = find_header_block(content, screen_prefix)
    if header_start is not None:
        header_block = content[header_start:header_end]
        # Determine the indentation
        first_line = header_block.split('\n')[0]
        indent = len(first_line) - len(first_line.lstrip())
        indent_str = ' ' * indent
        
        # Extract properties from the existing header
        # Look for title, showback, showsearch patterns
        title_match = re.search(r'Text:\s*="([^"]*)"', header_block)
        title = title_match.group(1) if title_match else screen_name.replace('_', ' ')
        
        show_back = 'true' if 'Back' in header_block or 'ShowBack' in header_block else 'false'
        show_search = 'true' if 'Search' in header_block or 'ShowSearch' in header_block else 'true'
        
        # Create component reference
        component_ref = f"""{indent_str}- {screen_prefix}AppHeader:
{indent_str}    Control: CanvasComponent
{indent_str}    ComponentName: cmp_AppHeader
{indent_str}    Properties:
{indent_str}      PageTitle: =\"{title}\"
{indent_str}      ShowBack: ={show_back}
{indent_str}      ShowSearch: ={show_search}"""
        
        content = content[:header_start] + component_ref + content[header_end:]
        print(f"  {screen_name}: Replaced header with cmp_AppHeader")
    
    # Write the modified content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    src_dir = 'src/Src'
    
    # Get all screen files
    screen_files = [f for f in os.listdir(src_dir) if f.startswith('scr_') and f.endswith('.pa.yaml')]
    
    print("Converting screens to use components...")
    for screen_file in sorted(screen_files):
        filepath = os.path.join(src_dir, screen_file)
        screen_name = screen_file.replace('.pa.yaml', '')
        print(f"\nProcessing {screen_name}...")
        convert_screen_to_components(filepath, screen_name)
    
    print("\nDone! All screens converted to use components.")

if __name__ == '__main__':
    main()
