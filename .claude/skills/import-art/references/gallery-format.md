# Gallery page format

## A normal piece

Add inside `<main class="wall">`, before the linked pieces at the end. Only the first figure omits `loading="lazy"`.

```html
<figure class="work">
  <a href="images/full/kakariki.jpg"><img src="images/thumb/kakariki.jpg" width="699" height="590" loading="lazy" alt="Bright green parakeet with a red crown perched on a twig, drawn on lined notepaper."></a>
  <figcaption><cite>Kākāriki</cite><span>Coloured pencil on notepaper</span></figcaption>
</figure>
```

`width`/`height` are the thumbnail's pixel size (printed by `process_art.py`).

## A colouring with credited line art

```html
<figcaption><cite>In Bloom</cite><span>Coloured pencil on a colouring page, line art by an unknown artist</span></figcaption>
```

If the line art is by a known artist, name them and the book: `Coloured pencil. Line art from <em>Small Victories</em> by Johanna Basford`.
The footer already says "All rights reserved, except for third-party line art noted in captions"; keep it that way.

## A piece shared on another site (linked piece)

Used for Johanna Basford colourings, which she asks to be shared through her gallery and social media rather than
rehosted. The image is hosted elsewhere and the figure links out. `gallery.js` falls back to the Instagram link
when the image fails to load.

```html
<figure class="work work-linked" data-instagram="https://www.instagram.com/p/POST_ID/">
  <a href="https://www.instagram.com/p/POST_ID/" target="_blank" rel="noopener"><img src="IMAGE_URL" width="1000" height="1000" alt="..."></a>
  <figcaption><cite>Moths</cite><span>Coloured pencil. Line art from <em>Small Victories</em> by Johanna Basford</span><a class="work-source" href="https://www.instagram.com/p/POST_ID/" target="_blank" rel="noopener">View on Instagram</a></figcaption>
</figure>
```

Posting to someone else's site or to Instagram is public and under the user's name: get the user's approval of
each caption first, and the user must log in themselves. Uploads to johannabasford.com wait for her review; link
to the Instagram post until her page for the piece is approved.

## Link preview

`og:image`, `og:image:width`, `og:image:height` and `og:image:alt` in `<head>` point at the first piece's
`images/full` file. Change them together with the first figure.
