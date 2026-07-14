// Типы для пользователя
export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    phone: string;
    department: string;
    position: string;
    role: 'admin' | 'teacher' | 'user' | 'guest';
    is_staff?: boolean;
}

export interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

// Типы для категории
export interface Category {
    id: number;
    name: string;
    slug: string;
    description: string;
    icon: string;
    created_at: string;
}

// Типы для ресурса
export interface Resource {
    id: number;
    name: string;
    description: string;
    category: Category;
    total_quantity: number;
    image: string | null;
    is_active: boolean;
    location: string;
    specifications: Record<string, any>;
    is_unique: boolean;
    created_at: string;
}

// Типы для бронирования
export interface Booking {
    id: number;
    user: User;
    resource: Resource;
    date: string;
    start_time: string;
    end_time: string;
    quantity: number;
    status: 'pending' | 'confirmed' | 'rejected' | 'completed' | 'cancelled';
    comment: string;
    admin_comment: string;
    created_at: string;
    updated_at: string;
}

// Тип для создания бронирования
export interface BookingCreate {
    resource: number;
    date: string;
    start_time: string;
    end_time: string;
    quantity: number;
    comment?: string;
}

// Тип для регистрации
export interface RegisterData {
    username: string;
    password: string;
    password2: string;
    email: string;
    first_name?: string;
    last_name?: string;
    phone?: string;
    department?: string;
    position?: string;
    role?: 'user' | 'teacher';
}

// Тип для входа
export interface LoginData {
    username: string;
    password: string;
}

// Тип для ответа с токеном
export interface AuthResponse {
    user: User;
    access: string;
    refresh: string;
}

// Тип для проверки доступности
export interface AvailabilityResponse {
    is_available: boolean;
    message: string;
    available_count: number;
}