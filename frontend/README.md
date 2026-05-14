# React + TypeScript + Vite

## Lệnh chạy nhanh

### Backend (Django)

```powershell
..\.venv\Scripts\Activate.ps1
python.exe manage.py runserver 8000
```

### Frontend (Vite)

```powershell
cd frontend
npm install
npm run dev
```

## Cấu hình môi trường

Tạo file `.env` trong thư mục `frontend` và khai báo URL backend:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

Mẫu này cung cấp cấu hình tối thiểu để React chạy được với Vite (HMR) và một số quy tắc ESLint.

Hiện tại có 2 plugin chính thức:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) sử dụng [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) sử dụng [SWC](https://swc.rs/)

## React Compiler

React Compiler không được bật sẵn vì ảnh hưởng tới hiệu năng khi dev và build. Nếu cần, xem [hướng dẫn này](https://react.dev/learn/react-compiler/installation).

## Mở rộng cấu hình ESLint

Nếu bạn phát triển ứng dụng production, nên cập nhật cấu hình để bật quy tắc lint có nhận biết kiểu:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Các cấu hình khác...

      // Bỏ tseslint.configs.recommended và thay bằng cấu hình này
      tseslint.configs.recommendedTypeChecked,
      // Hoặc dùng cái này nếu muốn stricter
      tseslint.configs.strictTypeChecked,
      // Tùy chọn: thêm quy tắc style
      tseslint.configs.stylisticTypeChecked,

      // Các cấu hình khác...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // tùy chọn khác...
    },
  },
])
```

Bạn có thể cài [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) và [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) cho quy tắc lint riêng của React:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Các cấu hình khác...
      // Bật quy tắc lint cho React
      reactX.configs['recommended-typescript'],
      // Bật quy tắc lint cho React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // tùy chọn khác...
    },
  },
])
```
