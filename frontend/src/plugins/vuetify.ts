// src/plugins/vuetify.ts
import 'vuetify/styles'; // Importa los estilos de Vuetify
import { createVuetify } from 'vuetify';
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "vuetify/styles";
import '@mdi/font/css/materialdesignicons.css';

import { aliases, mdi } from 'vuetify/iconsets/mdi';

export default createVuetify({
    directives,
    theme: {
        defaultTheme: "dark",
    },
    components: {
        ...components,
    },
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi
        }
    }
});