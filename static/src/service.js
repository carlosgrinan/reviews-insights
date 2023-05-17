// /** @odoo-module */

// import { registry } from "@web/core/registry";
// import { memoize } from "@web/core/utils/functions";

// export const sourceService = {
//     dependencies: ["rpc"],
//     async: ["loadSources"],
//     start(env, { rpc }) {
//         return {
//             loadSources: memoize(() => rpc("/proyecto_dam/source")),
//         };
//     },
// };

// registry.category("services").add("sourceService", sourceService);