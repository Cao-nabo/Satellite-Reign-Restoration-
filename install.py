"""Version-checked installation/removal for the combined SR Restoration market release."""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess

BACKUP = '.sr-restoration-market-backup'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def destination(root,relative):
    path=root/relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Payload path escapes game folder: '+relative)
    return path
def require_closed(game):
    if os.name=='nt':
        output=subprocess.check_output(['tasklist','/FI','IMAGENAME eq SatelliteReignWindows.exe','/FO','CSV','/NH'],text=True)
        if any(row and row[0].lower()=='satellitereignwindows.exe' for row in csv.reader(io.StringIO(output))):
            raise RuntimeError('Close Satellite Reign before changing game files.')
    elif Path('/proc').exists():
        wanted=str(game.resolve()).replace('\\','/').lower()
        for proc in Path('/proc').iterdir():
            try:
                if proc.name.isdigit() and (proc/'comm').read_text().startswith('SatelliteReign'):
                    command=(proc/'cmdline').read_bytes().replace(b'\\',b'/').decode(errors='replace').lower()
                    if wanted in command:
                        raise RuntimeError('Close this game copy before changing its files.')
            except (OSError,PermissionError):
                pass

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game',type=Path,required=True,help='Folder containing SatelliteReignWindows.exe')
    parser.add_argument('--uninstall',action='store_true')
    parser.add_argument('--check',action='store_true',help='Read-only compatibility check')
    args=parser.parse_args();game=args.game.resolve();release=Path(__file__).resolve().parent
    backup=game/BACKUP
    if not (game/'SatelliteReignWindows.exe').is_file():
        parser.error('Choose the Windows game folder, not its Data folder.')
    if args.uninstall:
        state=json.loads((backup/'state.json').read_text())
        for relative,entry in state.items():
            target=destination(game,relative)
            if entry['previous'] and sha(backup/'files'/relative)!=entry['previous_sha256']:
                raise RuntimeError('Backup hash mismatch; removal stopped: '+relative)
            if not target.is_file() or sha(target)!=entry['installed']:
                raise RuntimeError('Installed file changed; removal stopped: '+relative)
        if args.check:
            print('Removal check passed.');return
        require_closed(game)
        for relative,entry in state.items():
            target=destination(game,relative)
            if entry['previous']:
                shutil.copy2(backup/'files'/relative,target)
            else:
                target.unlink()
        shutil.rmtree(backup)
        print('Previous game/mod files restored; saves were not changed.');return
    manifest=json.loads((release/'manifest.json').read_text())
    core=game/'SatelliteReignWindows_Data/Managed/Assembly-CSharp.dll'
    if sha(core) not in manifest['accepted_install_core_hashes']:
        raise RuntimeError('Unsupported or differently modified core; installation stopped.')
    if backup.exists():
        raise RuntimeError('A market backup already exists; remove that installation first.')
    payload={name:digest for name,digest in manifest['files'].items() if name.startswith(('Mods/','SatelliteReignWindows_Data/Managed/'))}
    for relative,digest in payload.items():
        source=destination(release,relative);destination(game,relative)
        if sha(source)!=digest:
            raise RuntimeError('Release file hash mismatch: '+relative)
    if args.check:
        print('Compatible core and complete verified payload; no files changed.');return
    require_closed(game)
    backup.mkdir();state={}
    try:
        for relative,digest in payload.items():
            target=destination(game,relative);previous=target.exists()
            if previous:
                saved=backup/'files'/relative;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
            state[relative]={'previous':previous,'previous_sha256':sha(target) if previous else None,'installed':digest}
        (backup/'state.json').write_text(json.dumps(state,indent=2)+'\n')
    except Exception:
        shutil.rmtree(backup)
        raise
    changed=[]
    try:
        for relative in payload:
            target=destination(game,relative);target.parent.mkdir(parents=True,exist_ok=True)
            temporary=target.with_name(target.name+'.sr-market-tmp')
            shutil.copy2(release/relative,temporary);os.replace(temporary,target);changed.append(relative)
    except Exception:
        for relative in reversed(changed):
            target=destination(game,relative)
            if state[relative]['previous']:shutil.copy2(backup/'files'/relative,target)
            else:target.unlink()
        for relative in payload:
            temporary=destination(game,relative).with_name(Path(relative).name+'.sr-market-tmp')
            if temporary.exists():temporary.unlink()
        shutil.rmtree(backup)
        raise
    print('Combined restoration + market installed. Backup: '+str(backup))

if __name__=='__main__':
    main()
