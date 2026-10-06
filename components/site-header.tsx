import { getSearchIndex } from "@/lib/content";
import { HeaderClient } from "./header-client";

/** Server shell: loads the search index once, hands it to the client header. */
export function SiteHeader() {
  return <HeaderClient entries={getSearchIndex()} />;
}
