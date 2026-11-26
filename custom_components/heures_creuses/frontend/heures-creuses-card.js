/* Carte « Heures Creuses » — fournie avec l'intégration (aucune ressource à ajouter).
 * Utilisation :
 *   type: custom:heures-creuses-card
 *   entity: sensor.heures_creuses_periode
 */
const HC_CARD_VERSION = "1.3.0";

class HeuresCreusesCard extends HTMLElement {
  setConfig(config) {
    if (!config || !config.entity) {
      throw new Error("Paramètre 'entity' requis (ex : sensor.heures_creuses_periode)");
    }
    this._config = {
      color_hc: "#1e88e5",
      color_hp: "#e53935",
      compact: false,
      show_next: true,
      show_season: true,
      show_price: true,
      size: "normal", // small | normal | large
      ...config,
    };
    this._key = null;
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    this._build();
    this._update();
  }

  set hass(hass) {
    this._hass = hass;
    this._update();
  }

  getCardSize() {
    return this._config && this._config.compact ? 1 : 3;
  }

  getGridOptions() {
    return this._config && this._config.compact
      ? { columns: 12, rows: 1, min_columns: 4, min_rows: 1 }
      : { columns: 12, rows: 3, min_columns: 4, min_rows: 2 };
  }

  static getStubConfig(hass) {
    const id = Object.keys(hass.states).find(
      (k) =>
        k.startsWith("sensor.") &&
        hass.states[k].attributes &&
        hass.states[k].attributes.couleur !== undefined &&
        hass.states[k].attributes.prix !== undefined
    );
    return { entity: id || "sensor.heures_creuses_periode" };
  }

  _build() {
    const scale = { small: 0.8, normal: 1, large: 1.6 }[this._config.size] || 1;
    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; }
        ha-card {
          overflow: hidden; height: 100%;
          container-type: inline-size;
        }
        .box {
          --s: ${scale};
          box-sizing: border-box; height: 100%; min-height: 96px; width: 100%;
          display: flex; flex-direction: column; align-items: center; justify-content: center;
          gap: .35em; padding: 1em; text-align: center; color: #fff; cursor: pointer;
          transition: background .4s ease;
        }
        .title { font-weight: 700; line-height: 1.15;
          font-size: calc(clamp(1.2rem, 9cqw, 2.6rem) * var(--s)); }
        .price { font-size: calc(clamp(1rem, 6cqw, 1.7rem) * var(--s)); }
        .next  { font-size: calc(clamp(.8rem, 3.6cqw, 1.05rem) * var(--s)); opacity: .92; }
        .badge { font-size: calc(clamp(.7rem, 3cqw, .9rem) * var(--s));
          background: rgba(255,255,255,.22); padding: .15em .8em; border-radius: 2em; }
        .hidden { display: none; }
        .compact { flex-direction: row; flex-wrap: wrap; gap: .2em .9em; min-height: 0; padding: .6em 1em; }
        .compact .title { font-size: calc(clamp(1rem, 5cqw, 1.3rem) * var(--s)); }
        .compact .price { font-size: calc(clamp(.9rem, 4cqw, 1.1rem) * var(--s)); }
        .compact .next, .compact .badge { display: none; }
      </style>
      <ha-card>
        <div class="box ${this._config.compact ? "compact" : ""}">
          <div class="title"></div>
          <div class="price"></div>
          <div class="next"></div>
          <div class="badge"></div>
        </div>
      </ha-card>`;
    this.shadowRoot.querySelector(".box").addEventListener("click", () => {
      this.dispatchEvent(
        new CustomEvent("hass-more-info", {
          detail: { entityId: this._config.entity },
          bubbles: true,
          composed: true,
        })
      );
    });
  }

  _update() {
    const h = this._hass;
    const c = this._config;
    if (!h || !c || !this.shadowRoot) return;
    const st = h.states[c.entity];
    const key = JSON.stringify([
      st && st.state,
      st && st.attributes,
      c,
    ]);
    if (key === this._key) return;
    this._key = key;

    const q = (s) => this.shadowRoot.querySelector(s);
    const box = q(".box");
    const title = q(".title");
    const price = q(".price");
    const next = q(".next");
    const badge = q(".badge");

    if (!st) {
      box.style.background = "#757575";
      title.textContent = "Entité introuvable";
      price.textContent = c.entity;
      next.classList.add("hidden");
      badge.classList.add("hidden");
      return;
    }
    if (st.state === "unavailable" || st.state === "unknown") {
      box.style.background = "#757575";
      title.textContent = "Indisponible";
      price.textContent = "";
      next.classList.add("hidden");
      badge.classList.add("hidden");
      return;
    }

    const a = st.attributes || {};
    const hc = st.state === "Heure Creuse" || a.couleur === "bleu";
    box.style.background = hc ? c.color_hc : c.color_hp;
    title.textContent = (hc ? "🌙 " : "⚡ ") + (hc ? "Heure Creuse" : "Heure Pleine");

    const p = Number(a.prix);
    price.textContent = c.show_price && !isNaN(p) ? p.toFixed(4).replace(".", ",") + " €/kWh" : "";
    price.classList.toggle("hidden", !price.textContent);

    const m = Number(a.temps_restant_min);
    let txt = "";
    if (c.show_next && a.prochaine_periode && a.heure_prochain_changement) {
      txt = `${a.prochaine_periode} à ${a.heure_prochain_changement}`;
      if (!isNaN(m)) {
        txt += " · dans " + (m >= 60 ? `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, "0")}` : `${m} min`);
      }
    }
    next.textContent = txt;
    next.classList.toggle("hidden", !txt);

    const s = a.saison;
    const showS = c.show_season && (s === "Été" || s === "Hiver");
    badge.textContent = showS ? (s === "Été" ? "☀️ Mode Été" : "❄️ Mode Hiver") : "";
    badge.classList.toggle("hidden", !showS);
  }
}

if (!customElements.get("heures-creuses-card")) {
  customElements.define("heures-creuses-card", HeuresCreusesCard);
}
window.customCards = window.customCards || [];
if (!window.customCards.some((x) => x.type === "heures-creuses-card")) {
  window.customCards.push({
    type: "heures-creuses-card",
    name: "Heures Creuses",
    description: "Carte colorée Heure Creuse / Heure Pleine avec prix et prochain changement.",
    preview: false,
  });
}
console.info(`%c HEURES-CREUSES-CARD %c v${HC_CARD_VERSION} `, "background:#1e88e5;color:#fff", "background:#333;color:#fff");
