import { createClient } from '@supabase/supabase-js'

// Supabase設定
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

// Supabaseクライアントを作成
export const supabase = createClient(supabaseUrl, supabaseKey)

// Supabaseが有効かどうかをチェック
export const isSupabaseEnabled = () => {
  return supabaseUrl && supabaseKey
}

// 認証関連のヘルパー関数
export const auth = {
  // ユーザー情報を取得
  async getUser() {
    if (!isSupabaseEnabled()) return null
    
    const { data: { user } } = await supabase.auth.getUser()
    return user
  },

  // ログイン状態を監視
  onAuthStateChange(callback: (user: any) => void) {
    if (!isSupabaseEnabled()) return { data: { subscription: null } }
    
    return supabase.auth.onAuthStateChange((event, session) => {
      callback(session?.user || null)
    })
  },

  // メール/パスワードでサインアップ
  async signUp(email: string, password: string) {
    if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
    
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    })
    
    if (error) throw error
    return data
  },

  // メール/パスワードでサインイン
  async signIn(email: string, password: string) {
    if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
    
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    
    if (error) throw error
    return data
  },

  // サインアウト
  async signOut() {
    if (!isSupabaseEnabled()) return
    
    const { error } = await supabase.auth.signOut()
    if (error) throw error
  }
}

// データベース操作のヘルパー関数
export const db = {
  // Chat Bots
  chatBots: {
    async getAll() {
      if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
      
      const { data, error } = await supabase
        .from('chat_bots')
        .select('*')
        .order('created_at', { ascending: false })
      
      if (error) throw error
      return data
    },

    async create(chatBot: { name: string; color: string }) {
      if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
      
      const { data, error } = await supabase
        .from('chat_bots')
        .insert([chatBot])
        .select()
      
      if (error) throw error
      return data
    },

    async update(id: string, updates: { name?: string; color?: string }) {
      if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
      
      const { data, error } = await supabase
        .from('chat_bots')
        .update(updates)
        .eq('id', id)
        .select()
      
      if (error) throw error
      return data
    },

    async delete(id: string) {
      if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
      
      const { error } = await supabase
        .from('chat_bots')
        .delete()
        .eq('id', id)
      
      if (error) throw error
    }
  },

  // Cats
  cats: {
    async getAll() {
      if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
      
      const { data, error } = await supabase
        .from('cats')
        .select('*')
        .order('created_at', { ascending: false })
      
      if (error) throw error
      return data
    },

    async create(cat: { name: string; breed?: string; age?: number; weight?: number }) {
      if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
      
      const { data, error } = await supabase
        .from('cats')
        .insert([cat])
        .select()
      
      if (error) throw error
      return data
    },

    async update(id: string, updates: { name?: string; breed?: string; age?: number; weight?: number }) {
      if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
      
      const { data, error } = await supabase
        .from('cats')
        .update(updates)
        .eq('id', id)
        .select()
      
      if (error) throw error
      return data
    },

    async delete(id: string) {
      if (!isSupabaseEnabled()) throw new Error('Supabase is not configured')
      
      const { error } = await supabase
        .from('cats')
        .delete()
        .eq('id', id)
      
      if (error) throw error
    }
  }
}

export default supabase