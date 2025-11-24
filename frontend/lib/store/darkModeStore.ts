import { create } from "zustand";
import { persist } from "zustand/middleware";

interface DarkModeStore {
  isDark: boolean;
  toggle: () => void;
}

function applyTheme(isDark: boolean) {
  if (typeof window === "undefined") return;

  if (isDark) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
}

export const useDarkMode = create<DarkModeStore>()(
  persist(
    (set) => ({
      isDark: false,
      toggle: () =>
        set((state) => {
          const newDark = !state.isDark;
          applyTheme(newDark);
          return { isDark: newDark };
        }),
    }),
    {
      name: "dark-mode-storage",
      onRehydrateStorage: () => (state) => {
        if (state) {
          applyTheme(state.isDark);
        }
      },
    }
  )
);
