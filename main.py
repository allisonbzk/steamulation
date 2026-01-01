import sys
import json
import time
import os
import getpass
from PyQt5.QtWidgets import QApplication, QWizard, QWizardPage, QFileDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, QButtonGroup, QGroupBox, QHBoxLayout


class EmulatorPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle('Select Emulator')
        layout = QVBoxLayout()
        self.exe_path = QLineEdit()
        browse_btn = QPushButton('Browse...')
        browse_btn.clicked.connect(self.browse)
        layout.addWidget(QLabel('Emulator .exe:'))
        layout.addWidget(self.exe_path)
        layout.addWidget(browse_btn)
        self.setLayout(layout)
        self.exe_path.textChanged.connect(self.autofill_platform)
        # Autofill from config
        from PyQt5.QtCore import QTimer
        config = load_config()
        if config.get('last_emulator'):
            self.exe_path.setText(config['last_emulator'])
            # Delay autofill to ensure wizard/pages are fully initialized
            QTimer.singleShot(0, self.autofill_platform)

    def browse(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Select Emulator Executable', '', 'Executables (*.exe)')
        if path:
            self.exe_path.setText(path)

    def autofill_platform(self):
        exe = self.exe_path.text().lower()
        guess = guess_platform_from_exe(exe)
        # Set the platform name on the PlatformPage if not already filled
        wizard = self.wizard()
        if wizard:
            platform_page = wizard.page(2)  # Defensive: check type before access
            if hasattr(platform_page, 'platform_name'):
                if platform_page.platform_name.text().strip() == '':
                    platform_page.platform_name.setText(guess)
def get_mapping_path():
    return os.path.join(os.path.dirname(__file__), 'emulator_platform_map.json')

def load_mapping():
    try:
        with open(get_mapping_path(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # Default mapping if file doesn't exist
        return {
            "default": {
                'yuzu': 'Switch',
                'ryujinx': 'Switch',
                'eden': 'Switch',
                'citra': '3DS',
                'pcsx2': 'PS2',
                'dolphin': 'GameCube/Wii',
                'snes9x': 'SNES',
                'zsnes': 'SNES',
                'bsnes': 'SNES',
                'retroarch': 'RetroArch',
                'mame': 'Arcade',
                'epsxe': 'PS1',
                'duckstation': 'PS1',
                'melonDS': 'DS',
                'desmume': 'DS',
                'project64': 'N64',
                'cemu': 'Wii U',
                'rpcs3': 'PS3',
                'xemu': 'Xbox',
                'cxbx': 'Xbox',
                'openemu': 'Multi',
                'mednafen': 'Multi',
                'fceux': 'NES',
                'nestopia': 'NES',
                'visualboyadvance': 'GBA',
                'mgba': 'GBA',
                'no$gba': 'GBA',
                'mupen64': 'N64',
                'genplus': 'Genesis',
                'fusion': 'Genesis',
                'kega': 'Genesis',
                'ppsspp': 'PSP',
                'vita3k': 'Vita',
                'citra-qt': '3DS',
                'redream': 'Dreamcast',
                'flycast': 'Dreamcast',
                'openmsx': 'MSX',
                'fs-uae': 'Amiga',
                'vice': 'C64',
                'higan': 'Multi',
                'mess': 'Multi',
            },
            "custom": {}
        }

def save_mapping(mapping):
    with open(get_mapping_path(), 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)

def guess_platform_from_exe(exe):
    mapping = load_mapping()
    exe_base = os.path.basename(exe).lower()
    exe_key = os.path.splitext(exe_base)[0]
    # Check custom first
    for key, value in mapping.get('custom', {}).items():
        if key in exe_key:
            return value
    # Then default
    for key, value in mapping.get('default', {}).items():
        if key in exe_key:
            return value
    # Try to use an online API to guess the system
    try:
        guess = guess_platform_online(exe)
        if guess:
            # Save to custom mapping for future use
            mapping['custom'][exe_key] = guess
            save_mapping(mapping)
            return guess
    except Exception:
        pass
    # Fallback: use filename without extension, capitalized
    name = exe_key.capitalize()
    return name

# --- Online Guess Helper (placeholder) ---
def guess_platform_online(exe):
    """
    Try to guess the system/platform for an emulator executable using a web/AI API.
    This is a placeholder: insert your API call here (e.g., OpenAI, Bing, etc).
    Returns a string guess, or None if not found.
    """
    # Example: Use OpenAI API (pseudo-code, requires requests and an API key)
    # import requests
    # api_key = os.environ.get('OPENAI_API_KEY')
    # if not api_key:
    #     return None
    # prompt = f"What gaming system does the emulator '{exe}' run games for? Respond with only the system/platform name."
    # response = requests.post(
    #     'https://api.openai.com/v1/chat/completions',
    #     headers={'Authorization': f'Bearer {api_key}'},
    #     json={
    #         'model': 'gpt-3.5-turbo',
    #         'messages': [{'role': 'user', 'content': prompt}],
    #         'max_tokens': 10
    #     }
    # )
    # if response.ok:
    #     return response.json()['choices'][0]['message']['content'].strip()
    # return None
    return None  # No API key/configured, so always fallback


class RomsPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle('Select ROMs Folder')
        layout = QVBoxLayout()
        self.roms_path = QLineEdit()
        browse_btn = QPushButton('Browse...')
        browse_btn.clicked.connect(self.browse)
        layout.addWidget(QLabel('ROMs Folder:'))
        layout.addWidget(self.roms_path)
        layout.addWidget(browse_btn)
        self.setLayout(layout)
        # Autofill from config
        config = load_config()
        if config.get('last_roms'):
            self.roms_path.setText(config['last_roms'])
    def browse(self):
        path = QFileDialog.getExistingDirectory(self, 'Select ROMs Folder')
        if path:
            self.roms_path.setText(path)

class PlatformPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle('Platform Name')
        layout = QVBoxLayout()
        self.platform_name = QLineEdit()
        layout.addWidget(QLabel('Platform Name (e.g., SNES, PS2):'))
        layout.addWidget(self.platform_name)
        self.setLayout(layout)


class LaunchOptionsPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle('Launch Options')
        layout = QVBoxLayout()
        self.launch_options = QLineEdit()
        layout.addWidget(QLabel('Launch Options (use #rom as placeholder for ROM path):'))
        layout.addWidget(self.launch_options)
        layout.addWidget(QLabel('Example: -f -g #rom'))
        self.setLayout(layout)
        # Autofill from config
        config = load_config()
        if config.get('last_launch_options'):
            self.launch_options.setText(config['last_launch_options'])
        else:
            # Default value for first run
            self.launch_options.setText('#rom')


class IconOptionsPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle('Icon Options')
        layout = QVBoxLayout()
        
        # Fetch icons checkbox
        self.fetch_icons_check = QCheckBox('Fetch game icons from SteamGridDB')
        layout.addWidget(self.fetch_icons_check)
        
        # API key field
        layout.addWidget(QLabel('\nSteamGridDB API Key (optional):'))
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText('Enter your API key here')
        layout.addWidget(self.api_key_input)
        
        # Show/Hide password button
        show_key_layout = QHBoxLayout()
        self.show_key_check = QCheckBox('Show API key')
        self.show_key_check.stateChanged.connect(self.toggle_key_visibility)
        show_key_layout.addWidget(self.show_key_check)
        show_key_layout.addStretch()
        layout.addLayout(show_key_layout)
        
        # Instructions
        instructions = QLabel(
            'To fetch game icons, you need a free SteamGridDB API key.\n'
            'Get your API key at: https://www.steamgriddb.com/profile/preferences/api\n\n'
            'Note: Icon fetching is optional. Games will be added without icons if disabled.'
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet('color: #666; font-size: 9pt;')
        layout.addWidget(instructions)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Load saved settings
        config = load_config()
        self.fetch_icons_check.setChecked(config.get('fetch_icons', True))
        if config.get('steamgriddb_api_key'):
            self.api_key_input.setText(config['steamgriddb_api_key'])
    
    def toggle_key_visibility(self, state):
        if state:
            self.api_key_input.setEchoMode(QLineEdit.Normal)
        else:
            self.api_key_input.setEchoMode(QLineEdit.Password)


import re
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

class SummaryPage(QWizardPage):
    def __init__(self, wizard):
        super().__init__()
        self.setTitle('ROMs Found')
        self.wizard = wizard
        self.layout = QVBoxLayout()
        self.rom_list = QListWidget()
        self.layout.addWidget(QLabel('Games detected:'))
        self.layout.addWidget(self.rom_list)
        self.status_label = QLabel()
        self.layout.addWidget(self.status_label)
        self.setLayout(self.layout)
        # Mark this as the final page
        self.setFinalPage(True)
    
    def initializePage(self):
        # Hide Cancel button on this page
        self.wizard.button(QWizard.CancelButton).setVisible(False)
        # Change Finish button text to "Close"
        self.wizard.button(QWizard.FinishButton).setText('Close')
        # Create custom "Add to Steam Library" button in place of Next/Finish
        self.wizard.button(QWizard.CustomButton1).setText('Add to Steam Library')
        self.wizard.button(QWizard.CustomButton1).setVisible(True)
        self.wizard.button(QWizard.CustomButton1).clicked.connect(self.save_shortcuts)
        # Set button layout: [Back] [Finish->Close] ... [CustomButton1->Add to Steam]
        self.wizard.setOption(QWizard.HaveCustomButton1, True)

        # Scan for ROMs
        roms_folder = self.wizard.page(3).roms_path.text()  # RomsPage is at index 3
        games = scrape_roms(roms_folder)
        self.rom_list.clear()
        for game in games:
            item = QListWidgetItem(game['display_name'])
            item.setToolTip(game['path'])
            self.rom_list.addItem(item)
        self.wizard.found_games = games
        self.status_label.setText("")

    def save_shortcuts(self):
        emulator = self.wizard.page(1).exe_path.text()
        platform = self.wizard.page(2).platform_name.text()
        launch_options = self.wizard.page(4).launch_options.text()  # LaunchOptionsPage is at index 4
        fetch_icons = self.wizard.page(5).fetch_icons_check.isChecked()  # IconOptionsPage is at index 5
        api_key = self.wizard.page(5).api_key_input.text().strip()  # Get API key from IconOptionsPage
        games = self.wizard.found_games
        steamids = self.wizard.page(0).selected_steamids()
        
        # Validation
        if not emulator or not os.path.exists(emulator):
            self.status_label.setText("Error: Invalid emulator path")
            return
        if not platform.strip():
            self.status_label.setText("Error: Platform name required")
            return
        if not games:
            self.status_label.setText("Error: No games found")
            return
        if not steamids:
            self.status_label.setText("Error: No Steam user selected")
            return
        
        # Save last used paths
        config = load_config()
        config['last_emulator'] = emulator
        config['last_roms'] = self.wizard.page(3).roms_path.text()
        config['last_launch_options'] = launch_options
        config['fetch_icons'] = fetch_icons
        if api_key:
            config['steamgriddb_api_key'] = api_key
        if steamids:
            config['last_steamid'] = steamids[0]
        save_config(config)
        
        # Disable button during processing
        self.wizard.button(QWizard.CustomButton1).setEnabled(False)
        self.status_label.setText("Starting...")
        QApplication.processEvents()  # Update UI
        
        try:
            count = 0
            for steamid in steamids:
                count += add_steam_shortcuts(
                    emulator, 
                    platform.strip(), 
                    games, 
                    steamid, 
                    launch_options, 
                    fetch_icons,
                    progress_callback=self.update_progress
                )
            self.status_label.setText(f"✓ Successfully added/updated {count} shortcuts to Steam!")
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(error_details)  # Print full traceback to console
            self.status_label.setText(f"Error: {str(e)[:100]}...")  # Show truncated error
        finally:
            # Re-enable button
            self.wizard.button(QWizard.CustomButton1).setEnabled(True)
    
    def update_progress(self, message):
        """Update the status label with progress messages."""
        self.status_label.setText(message)
        QApplication.processEvents()  # Force UI update

def get_icons_cache_dir():
    """Get or create the icons cache directory."""
    cache_dir = os.path.join(os.path.dirname(__file__), 'icon_cache')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir

def sanitize_filename(name):
    """Sanitize game name for use as filename."""
    # Remove invalid filename characters
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def fetch_game_icon(game_name, appid, steamid, platform='switch', progress_callback=None):
    """Fetch game icon from SteamGridDB and save to Steam's grid folder."""
    try:
        import requests
        from urllib.parse import quote
        
        # Get Steam's grid folder for this user
        userdata_path = get_steam_userdata_path()
        grid_dir = os.path.join(userdata_path, steamid, 'config', 'grid')
        if not os.path.exists(grid_dir):
            os.makedirs(grid_dir)
        
        # Steam uses unsigned 32-bit AppID for grid filenames
        # Convert signed to unsigned for display
        unsigned_appid = int(appid) & 0xFFFFFFFF
        
        # Different artwork types - correct Steam naming convention
        grid_portrait_path = os.path.join(grid_dir, f"{unsigned_appid}p.png")  # Vertical grid (600x900)
        hero_path = os.path.join(grid_dir, f"{unsigned_appid}_hero.png")  # Hero background (1920x620)
        logo_path = os.path.join(grid_dir, f"{unsigned_appid}_logo.png")  # Logo overlay
        icon_path = os.path.join(grid_dir, f"{unsigned_appid}_icon.png")  # Icon
        grid_landscape_path = os.path.join(grid_dir, f"{unsigned_appid}.png")  # Horizontal grid (920x430)
        
        # Check if all already exist
        all_paths = [grid_portrait_path, grid_landscape_path, hero_path, icon_path, logo_path]
        if all(os.path.exists(p) for p in all_paths):
            msg = f"All artwork already exists for '{game_name}'"
            print(msg)
            if progress_callback:
                progress_callback(msg)
            # Return the icon path if it exists
            return icon_path if os.path.exists(icon_path) else None
        
        # Check for API key in environment or config
        api_key = os.environ.get('STEAMGRIDDB_API_KEY')
        if not api_key:
            config = load_config()
            api_key = config.get('steamgriddb_api_key')
        
        if not api_key:
            msg = f"⚠ Skipping '{game_name}' - No API key"
            print(msg)
            print("  Get a free API key at: https://www.steamgriddb.com/profile/preferences/api")
            print("  Set environment variable: STEAMGRIDDB_API_KEY=your_key")
            if progress_callback:
                progress_callback(msg)
            return None
        
        # Use SteamGridDB API with authentication
        search_term = quote(game_name)
        search_url = f"https://www.steamgriddb.com/api/v2/search/autocomplete/{search_term}"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        msg = f"Searching for '{game_name}'..."
        print(msg)
        if progress_callback:
            progress_callback(msg)
        
        response = requests.get(search_url, headers=headers, timeout=10)
        if not response.ok:
            msg = f"✗ Search failed for '{game_name}'"
            print(msg)
            if progress_callback:
                progress_callback(msg)
            return None
        
        data = response.json()
        if not (data.get('success') and data.get('data') and len(data['data']) > 0):
            msg = f"✗ No results for '{game_name}'"
            print(msg)
            if progress_callback:
                progress_callback(msg)
            return None
        
        # Get the first match's game ID
        game_id = data['data'][0].get('id')
        if not game_id:
            msg = f"✗ No game ID for '{game_name}'"
            print(msg)
            if progress_callback:
                progress_callback(msg)
            return None
        
        success_count = 0
        
        # Fetch different artwork types with proper filtering
        # Note: grids endpoint returns both portrait and landscape, need to filter by dimensions
        artwork_requests = [
            ('grids', grid_portrait_path, 'portrait grid', 'portrait'),  # 600x900 or similar
            ('grids', grid_landscape_path, 'landscape grid', 'landscape'),  # 920x430 or similar
            ('heroes', hero_path, 'hero/background', None),
            ('icons', icon_path, 'icon', None),
            ('logos', logo_path, 'logo', None)
        ]
        
        print(f"Will save artwork to:")
        print(f"  Portrait: {grid_portrait_path}")
        print(f"  Landscape: {grid_landscape_path}")
        print(f"  Hero: {hero_path}")
        print(f"  Icon: {icon_path}")
        print(f"  Logo: {logo_path}")
        
        for endpoint, save_path, art_name, dimension_filter in artwork_requests:
            if os.path.exists(save_path):
                print(f"  {art_name} already exists")
                success_count += 1
                continue
            
            try:
                # Different API endpoints for different art types
                art_url = f"https://www.steamgriddb.com/api/v2/{endpoint}/game/{game_id}"
                
                print(f"  Fetching {art_name}...")
                art_response = requests.get(art_url, headers=headers, timeout=10)
                
                if art_response.ok:
                    art_data = art_response.json()
                    
                    if art_data.get('success') and art_data.get('data') and len(art_data['data']) > 0:
                        # For grids, filter by aspect ratio (portrait vs landscape)
                        # Portrait: height > width (typically 600x900)
                        # Landscape: width > height (typically 920x430)
                        available_images = art_data['data']
                        
                        if dimension_filter:
                            filtered = []
                            for img in available_images:
                                w, h = img.get('width', 0), img.get('height', 0)
                                if dimension_filter == 'portrait' and h > w:
                                    filtered.append(img)
                                elif dimension_filter == 'landscape' and w > h:
                                    filtered.append(img)
                            
                            if filtered:
                                available_images = filtered
                            else:
                                print(f"  ✗ No {dimension_filter} {art_name} available")
                                continue
                        
                        # Get the first image URL
                        img_url = available_images[0].get('url')
                        if img_url:
                            msg = f"Downloading {art_name} for '{game_name}'..."
                            print(msg)
                            if progress_callback:
                                progress_callback(msg)
                            
                            # Don't send Authorization to CDN - use basic headers only
                            img_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                            img_response = requests.get(img_url, headers=img_headers, timeout=15)
                            if img_response.ok:
                                with open(save_path, 'wb') as f:
                                    f.write(img_response.content)
                                print(f"  ✓ {art_name} downloaded to {os.path.basename(save_path)}")
                                success_count += 1
                            else:
                                print(f"  ✗ Failed to download {art_name}: HTTP {img_response.status_code}")
                        else:
                            print(f"  ✗ No URL for {art_name}")
                    else:
                        print(f"  ✗ No {art_name} data available")
                else:
                    print(f"  ✗ Failed to fetch {art_name}: HTTP {art_response.status_code}")
            except Exception as e:
                print(f"  ✗ Failed to download {art_name}: {e}")
                import traceback
                traceback.print_exc()
        
        if success_count > 0:
            msg = f"✓ Downloaded {success_count}/5 artwork types for '{game_name}'"
            print(msg)
            if progress_callback:
                progress_callback(msg)
            # Return the icon path if it exists
            return icon_path if os.path.exists(icon_path) else None
        else:
            msg = f"✗ No artwork downloaded for '{game_name}'"
            print(msg)
            if progress_callback:
                progress_callback(msg)
            return None
            
    except Exception as e:
        msg = f"✗ Failed to fetch artwork for '{game_name}': {e}"
        print(msg)
        import traceback
        traceback.print_exc()
        if progress_callback:
            progress_callback(msg)
        return None

def scrape_roms(roms_folder):
    # Recursively find .nsp files, avoid updates, extract display name
    games = []
    for root, dirs, files in os.walk(roms_folder):
        for file in files:
            if file.lower().endswith('.nsp'):
                if '[v0]' not in file.lower():
                    continue  # Only accept base version [v0], skip all updates
                # Extract display name: everything before the first ' ['
                base = os.path.splitext(file)[0]
                split_idx = base.find(' [')
                if split_idx > 0:
                    display_name = base[:split_idx].strip()
                else:
                    display_name = base
                games.append({
                    'display_name': display_name,
                    'path': os.path.join(root, file)
                })
    return games

# --- Steam Shortcuts Logic ---
import vdf

def get_steam_userdata_path():
    # Default Steam path for Windows
    user = getpass.getuser()
    possible_paths = [
        os.path.expandvars(rf'C:\Program Files (x86)\Steam\userdata'),
        os.path.expandvars(rf'C:\Program Files\Steam\userdata'),
        os.path.expandvars(rf'D:\Steam\userdata'),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError('Could not find Steam userdata folder.')

def get_steam_users():
    """
    Returns a list of dicts: [{ 'steamid': ..., 'personaname': ... }]
    """
    users = []
    userdata_path = get_steam_userdata_path()
    for user_id in os.listdir(userdata_path):
        if not user_id.isdigit():
            continue
        config_path = os.path.join(userdata_path, user_id, 'config', 'localconfig.vdf')
        persona = user_id
        if os.path.exists(config_path):
            try:
                import vdf
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = vdf.load(f)
                persona = data.get('UserLocalConfigStore', {}).get('friends', {}).get('PersonaName', user_id)
            except Exception:
                pass
        users.append({'steamid': user_id, 'personaname': persona})
    return users

class SteamUserPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle('Select Steam User(s)')
        layout = QVBoxLayout()
        self.user_checks = []
        self.user_group = QGroupBox('Steam Users')
        self.user_layout = QVBoxLayout()
        self.user_group.setLayout(self.user_layout)
        layout.addWidget(self.user_group)
        self.setLayout(layout)

    def initializePage(self):
        # Clear previous
        for i in reversed(range(self.user_layout.count())):
            widget = self.user_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.user_checks = []
        users = get_steam_users()
        config = load_config()
        last_user = config.get('last_steamid')
        for user in users:
            cb = QCheckBox(f"{user['personaname']} ({user['steamid']})")
            cb.steamid = user['steamid']
            if last_user and user['steamid'] == last_user:
                cb.setChecked(True)
            self.user_layout.addWidget(cb)
            self.user_checks.append(cb)
        # If no last user, check the first by default
        if users and not any(cb.isChecked() for cb in self.user_checks):
            self.user_checks[0].setChecked(True)

    def selected_steamids(self):
        return [cb.steamid for cb in self.user_checks if cb.isChecked()]

def find_steam_shortcuts_vdf(steamid=None):
    userdata_path = get_steam_userdata_path()
    # Find the user folder (should be the SteamID)
    if steamid:
        config_path = os.path.join(userdata_path, steamid, 'config')
        if os.path.isdir(config_path):
            vdf_path = os.path.join(config_path, 'shortcuts.vdf')
            return vdf_path
        raise FileNotFoundError(f'Could not find shortcuts.vdf for SteamID {steamid}')
    # Fallback: first user
    for user_id in os.listdir(userdata_path):
        config_path = os.path.join(userdata_path, user_id, 'config')
        if os.path.isdir(config_path):
            vdf_path = os.path.join(config_path, 'shortcuts.vdf')
            return vdf_path
    raise FileNotFoundError('Could not find shortcuts.vdf in any Steam user config.')

def add_shortcuts_to_steam_collection(appids, collection_name, steamid=None):
    import json
    import time
    print(f"Adding appids {appids} to collection '{collection_name}' for steamid {steamid}")
    # Find cloud-storage-namespace-1.json for the user
    userdata_path = get_steam_userdata_path()
    if not steamid:
        # fallback: first user
        for user_id in os.listdir(userdata_path):
            config_path = os.path.join(userdata_path, user_id, 'config', 'cloudstorage')
            json_path = os.path.join(config_path, 'cloud-storage-namespace-1.json')
            if os.path.exists(json_path):
                steamid = user_id
                break
    config_path = os.path.join(userdata_path, steamid, 'config', 'cloudstorage')
    json_path = os.path.join(config_path, 'cloud-storage-namespace-1.json')
    if not os.path.exists(json_path):
        print(f"JSON file not found at {json_path}")
        return  # Can't add to collection if file doesn't exist
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Find or create the collection by name
    found = False
    for entry in data:
        key, value = entry
        if key.startswith('user-collections.'):
            v = value.get('value')
            if not v:
                continue
            try:
                vobj = json.loads(v)
            except Exception:
                continue
            print(f"Checking collection '{vobj.get('name')}'")
            if vobj.get('name') == collection_name:
                print(f"Found existing collection '{collection_name}'")
                # Add appids to 'added' array as integers if not present
                added = vobj.setdefault('added', [])
                initial_count = len(added)
                changed = False
                for appid in appids:
                    appid_int = int(appid)
                    if appid_int not in [int(a) for a in added]:
                        added.append(appid_int)
                        changed = True
                        print(f"  Adding appid {appid_int}")
                
                if changed:
                    # Remove duplicates and sort
                    vobj['added'] = sorted(set(int(a) for a in added))
                    # Update the value with new JSON
                    value['value'] = json.dumps(vobj, separators=(',', ':'))
                    # Update timestamp to trigger Steam to reload
                    value['timestamp'] = int(time.time())
                    # Increment version number
                    current_version = int(value.get('version', '0'))
                    value['version'] = str(current_version + 1)
                    print(f"  Updated collection: {len(vobj['added']) - initial_count} new games added (total: {len(vobj['added'])})")
                else:
                    print(f"  No new games to add (all already in collection)")
                found = True
                break
    if not found:
        print(f"Creating new collection '{collection_name}'")
        # Create a new static collection entry
        new_id = f"uc-{int(time.time() * 1000):x}"
        vobj = {
            "id": new_id,
            "name": collection_name,
            "added": sorted(set(int(a) for a in appids)),
            "removed": [],
            # For static collections, do NOT include filterSpec
        }
        # Find the next version number
        max_version = 0
        for entry in data:
            if isinstance(entry, list) and len(entry) > 1:
                ver = entry[1].get('version')
                if ver and ver.isdigit():
                    max_version = max(max_version, int(ver))
        next_version = str(max_version + 1)
        entry = [f"user-collections.{new_id}", {
            "key": f"user-collections.{new_id}",
            "timestamp": int(time.time()),
            "value": json.dumps(vobj, separators=(',', ':')),
            "version": next_version,
            "strMethodId": "static"
        }]
        data.append(entry)
    # Sort collections so new ones are not at the end (Steam expects sorted by key)
    data.sort(key=lambda x: x[0] if isinstance(x, list) and len(x) > 0 else str(x))
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))
    print(f"Updated cloud-storage-namespace-1.json with collection '{collection_name}'")

def add_steam_shortcuts(emulator, platform, games, steamid=None, launch_options_template='#rom', fetch_icons=True, progress_callback=None):
    vdf_path = find_steam_shortcuts_vdf(steamid)
    # Read existing shortcuts robustly
    shortcut_dict = {}
    if os.path.exists(vdf_path):
        try:
            with open(vdf_path, 'rb') as f:
                shortcuts = vdf.binary_load(f)
            shortcut_dict = shortcuts.get('shortcuts', {})
            if not isinstance(shortcut_dict, dict):
                shortcut_dict = {}
        except Exception:
            shortcut_dict = {}
    shortcut_list = list(shortcut_dict.values())
    updated = 0
    new_appids = []
    # First pass: collect appids and mark updates
    for game in games:
        appid = calc_shortcut_appid(emulator.replace('/', '\\'), game['display_name'])
        # Convert to unsigned 32-bit integer for collection management
        new_appids.append(int(appid) & 0xFFFFFFFF)
        updated += 1
    # Remove duplicates from new_appids
    new_appids = sorted(set(new_appids))
    # Second pass: write/update shortcuts
    total_games = len(games)
    for idx, game in enumerate(games, 1):
        # Update progress
        if progress_callback:
            progress_callback(f"Processing {idx}/{total_games}: {game['display_name']}")
        
        # Fetch icon if enabled (save directly to Steam's grid folder)
        icon_path = None
        if fetch_icons:
            appid = calc_shortcut_appid(emulator.replace('/', '\\'), game['display_name'])
            icon_path = fetch_game_icon(game['display_name'], appid, steamid, platform.lower(), progress_callback)
        
        found = False
        for s in shortcut_list:
            if s.get('AppName') == game['display_name'] or s.get('appname') == game['display_name']:
                s['AppName'] = game['display_name']
                s['Exe'] = f'"{emulator}"'.replace('/', '\\')
                s['StartDir'] = f'"{os.path.dirname(emulator)}"'.replace('/', '\\')
                s['LaunchOptions'] = launch_options_template.replace('#rom', f'"{game["path"]}"')
                s['LastPlayTime'] = int(time.time())
                s['DevkitOverrideAppID'] = 0
                s['FlatpakAppID'] = ''
                s['sortas'] = ''
                s['tags'] = {}
                s['appid'] = calc_shortcut_appid(emulator.replace('/', '\\'), game['display_name'])
                # Set icon path if we have one
                if icon_path:
                    s['icon'] = icon_path
                # Remove lowercase keys if present
                if 'appname' in s:
                    del s['appname']
                if 'exe' in s:
                    del s['exe']
                found = True
                break
        if not found:
            shortcut = {
                'AppName': game['display_name'],
                'Exe': f'"{emulator}"'.replace('/', '\\'),
                'StartDir': f'"{os.path.dirname(emulator)}"'.replace('/', '\\'),
                'icon': icon_path if icon_path else '',
                'ShortcutPath': '',
                'LaunchOptions': launch_options_template.replace('#rom', f'"{game["path"]}"'),
                'IsHidden': 0,
                'AllowDesktopConfig': 1,
                'AllowOverlay': 1,
                'OpenVR': 0,
                'Devkit': 0,
                'DevkitGameID': '',
                'DevkitOverrideAppID': 0,
                'LastPlayTime': int(time.time()),
                'FlatpakAppID': '',
                'sortas': '',
                'tags': {},
                'appid': calc_shortcut_appid(emulator.replace('/', '\\'), game['display_name'])
            }
            shortcut_list.append(shortcut)
    
    if progress_callback:
        progress_callback(f"Writing {len(shortcut_list)} shortcuts to Steam...")
    
    print(f"Writing shortcuts to {vdf_path}")
    shortcuts_dict = {'shortcuts': {str(i): s for i, s in enumerate(shortcut_list)}}
    with open(vdf_path, 'wb') as f:
        vdf.binary_dump(shortcuts_dict, f)
    print(f"Shortcuts written successfully")
    
    if progress_callback:
        progress_callback(f"Adding games to '{platform}' collection...")
    
    # Add to Steam static collection after shortcuts
    add_shortcuts_to_steam_collection(new_appids, platform, steamid)
    return updated

def calc_shortcut_appid(exe, appname):
    import zlib
    # Steam's algorithm: appid = crc32(exe + appname) | 0x80000000
    key = exe.encode('utf-8') + appname.encode('utf-8')
    crc = zlib.crc32(key) & 0xFFFFFFFF
    return str(crc | 0x80000000)
# --- Config persistence ---
def get_config_path():
    return os.path.join(os.path.dirname(__file__), 'steam_emu_config.json')

def load_config():
    try:
        with open(get_config_path(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(cfg):
    with open(get_config_path(), 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2)

class SteamEmuWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Steam Emulator Station Wizard')
        # Enable custom button but hide it by default
        self.setOption(QWizard.HaveCustomButton1, True)
        self.button(QWizard.CustomButton1).setVisible(False)
        self.addPage(SteamUserPage())           # Index 0
        self.addPage(EmulatorPage())            # Index 1
        self.addPage(PlatformPage())            # Index 2
        self.addPage(RomsPage())                # Index 3
        self.addPage(LaunchOptionsPage())       # Index 4
        self.addPage(IconOptionsPage())         # Index 5
        self.addPage(SummaryPage(self))         # Index 6
        self.found_games = []

def main():
    app = QApplication(sys.argv)
    wizard = SteamEmuWizard()
    wizard.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
