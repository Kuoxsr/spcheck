# sound-pack-checker
This is a personal tool to check whether `sounds.json` matches the `.ogg` files in the folder structure of a Minecraft resource pack.  I needed something to make this process quicker.

### what it does
The project currently produces several lists:

- Invalid file names: Names that don't match Minecraft's specifications
- Broken links: All the `.json` directives that don't link to any `.ogg` file
- Orphans: All the `.ogg` files that aren't mentioned in the `.json` file
- Aliens: All the files that are neither .ogg nor .json

