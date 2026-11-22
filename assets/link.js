// Duel (d) and friend invite (f) links. Accepted shapes, all shown the same way:
//   /d/CODE  (current; GitHub Pages answers it with 404.html)
//   /d/?c=CODE or /d/#CODE  (answered by /d/index.html with HTTP 200, so link previews work)
// When Brillion is installed, iOS opens these links in the app and this page never shows.
(function () {
  var path = location.pathname;
  var m = path.match(/^\/(d|f)\/([A-Za-z0-9]{6,8})\/?$/);
  var kind = m && m[1], code = m && m[2];
  if (!m) {
    var k = path.match(/^\/(d|f)\/?$/);
    if (k) {
      kind = k[1];
      var q = new URLSearchParams(location.search).get('c') || location.hash.replace(/^#/, '');
      if (/^[A-Za-z0-9]{6,8}$/.test(q || '')) code = q;
    }
  }
  if (!kind) return;
  var duel = kind === 'd';
  var card = document.getElementById('card');
  card.textContent = '';
  var p1 = document.createElement('p'); p1.className = 'lead';
  p1.textContent = duel ? "You've been challenged to a duel." : 'A friend wants to dive with you.';
  card.append(p1);
  if (code) {
    code = code.toUpperCase();
    var c = document.createElement('div'); c.className = 'code'; c.textContent = code;
    var p2 = document.createElement('p'); p2.className = 'muted';
    p2.textContent = duel ? 'Get Brillion, open Duels, and enter this code.' : 'Get Brillion, open Friends, and add this code.';
    card.append(c, p2);
  }
  var actions = document.querySelector('.actions');
  if (code && actions) {
    var a = document.createElement('a'); a.className = 'btn';
    a.href = 'brillion://' + kind + '/' + code; a.textContent = 'OPEN IN BRILLION';
    actions.append(a);
  }
})();
