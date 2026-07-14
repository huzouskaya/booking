import api from './api';

export const seedService = {
  // Создание тестовых данных
  async seedDatabase() {
    try {
      // 1. Создаём категории
      const categories = [
        { name: 'Аудитории', slug: 'auditorii', description: 'Учебные аудитории для проведения занятий', icon: 'classroom' },
        { name: 'Компьютерные классы', slug: 'kompyuternye-klassy', description: 'Компьютерные классы с доступом к интернету', icon: 'computer' },
        { name: 'Лаборатории', slug: 'laboratorii', description: 'Научные лаборатории с оборудованием', icon: 'science' },
        { name: 'Переговорные комнаты', slug: 'peregovornye', description: 'Комнаты для встреч и переговоров', icon: 'meeting' },
        { name: 'Оборудование', slug: 'oborudovanie', description: 'Проекторы, ноутбуки и другая техника', icon: 'equipment' },
      ];

      for (const cat of categories) {
        await api.post('bookings/categories/', cat);
      }

      // 2. Создаём ресурсы
      const resources = [
        {
          name: 'Аудитория 666',
          description: 'Большая аудитория на 100 мест с проектором и доской',
          category: 1,
          total_quantity: 1,
          location: 'Корпус 6, этаж 6',
          is_active: true,
          specifications: { capacity: 100, has_projector: true, has_whiteboard: true }
        },
        {
          name: 'Компьютерный класс №1408',
          description: '15 компьютеров с доступом к интернету и проектором',
          category: 2,
          total_quantity: 1,
          location: 'Корпус 1, этаж 4',
          is_active: true,
          specifications: { computers: 15, has_projector: true, os: 'Windows 11' }
        },
        {
          name: 'Лаборатория Виктора Франкенштейна',
          description: 'Научная лаборатория с микроскопами и реактивами',
          category: 3,
          total_quantity: 1,
          location: 'Корпус 5, этаж 2',
          is_active: true,
          specifications: { equipment: 'Микроскопы, реактивы, центрифуга' }
        },
        {
          name: 'Проектор Epson 13',
          description: '4K проектор для презентаций и лекций',
          category: 5,
          total_quantity: 3,
          location: 'Корпус 3, этаж 2',
          is_active: true,
          specifications: { resolution: '3840x2160', brightness: '4000 люмен', weight: '3.5 кг' }
        },
        {
          name: 'Ноутбук Hell Inspiron 16',
          description: 'Мощный ноутбук для работы и презентаций',
          category: 5,
          total_quantity: 5,
          location: 'Корпус 1, этаж 3',
          is_active: true,
          specifications: { processor: 'Intel Core i7', ram: '16GB', storage: '512GB SSD' }
        },
        {
          name: 'Переговорная комната 3.14',
          description: 'Комната для встреч на 8 человек с телевизором',
          category: 4,
          total_quantity: 1,
          location: 'Корпус 3, этаж 1',
          is_active: true,
          specifications: { capacity: 8, has_tv: true, has_whiteboard: true }
        },
      ];

      for (const res of resources) {
        await api.post('bookings/resources/', res);
      }

      return { success: true, message: 'Тестовые данные созданы!' };
    } catch (error) {
      console.error('Ошибка создания тестовых данных:', error);
      return { success: false, error };
    }
  }
};