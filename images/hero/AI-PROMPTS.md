# Hero slider images

The homepage slider is full width. To stay sharp on large screens, every image
needs to be **landscape, at least 2560 × 1280 px (2:1)**. 3840 × 1920 is better.
Images are cropped to fill the slider and never stretched, so any size at or
above that works.

Keep the **left 40% of each image calm** (soft, low detail, darker or plain):
the headline sits on top of it.

## How to swap images

1. Save each image as a JPG (quality around 80%, under 600 KB) in this folder.
2. Open `_build/data.py` and edit `HERO_SLIDES`: file name, caption, alt text,
   and `pos` (which part of the photo stays in view, e.g. `"70% 50%"`).
3. Run `python _build/build.py` from the `v2` folder.

## A note on honesty

Captions like "Plant II, Mujpur" tell visitors they are looking at the real
plant. Use AI images only with generic captions (for example "Mineral salts",
"Quality control"), and keep at least the first slide a real photo of the
plant. A professional photo shoot of Plant II at 4K is still the best option.

## Prompts

Tested style suffix (add to every prompt):

> photorealistic, editorial pharmaceutical photography, white and cool grey
> palette with deep indigo accents, soft diffused daylight, clean and minimal,
> high detail, 2:1 wide aspect ratio, negative space on the left third,
> no text, no logos, no people's faces

| # | File name | Caption | Prompt |
|---|---|---|---|
| 1 | `ai-crystals.jpg` | Mineral salts | Extreme macro of translucent white mineral salt crystals piled on the right side of a matte white surface, a few crystals catching a cool blue-violet rim light, shallow depth of field |
| 2 | `ai-powder.jpg` | Fine powders | Fine white pharmaceutical-grade powder on a stainless steel scoop, a soft heap with a smooth surface, set on brushed steel, right of frame, background out of focus |
| 3 | `ai-qc-lab.jpg` | Quality control | Modern quality control laboratory bench, glass volumetric flasks with clear solutions, an analytical balance, white cabinets, indigo-blue accent light, gloved hand pipetting at right edge only |
| 4 | `ai-cleanroom.jpg` | Clean manufacturing | Wide view of a bright pharmaceutical cleanroom corridor with epoxy floor, stainless steel equipment and blue airlock doors, symmetrical perspective, very clean |
| 5 | `ai-tablets.jpg` | Supplements | White mineral supplement tablets and capsules scattered on the right of a pale grey surface, soft shadows, top-down at a slight angle |

Midjourney: add `--ar 2:1 --style raw --q 2` and upscale (Upscale Subtle).
Adobe Firefly / DALL·E / Ideogram: choose the widest aspect ratio, then
upscale to 2560 px or more before saving.
