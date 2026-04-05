/**
 * @fileoverview Seed script to create a set of test users for all roles.
 * Uses the better-auth API to ensure correct password hashing and DB structure.
 */

import { auth } from "../src/lib/auth";

const testUsers = [
  { email: "admin@precognito.ai", password: "Password123!", name: "Admin User", role: "ADMIN" },
  { email: "manager@precognito.ai", password: "Password123!", name: "Plant Manager", role: "MANAGER" },
  { email: "ot@precognito.ai", password: "Password123!", name: "OT Specialist", role: "OT_SPECIALIST" },
  { email: "tech@precognito.ai", password: "Password123!", name: "Maintenance Tech", role: "TECHNICIAN" },
  { email: "store@precognito.ai", password: "Password123!", name: "Store Manager", role: "STORE_MANAGER" },
];

async function seedAll() {
  console.log("Seeding all role-based test users using Better Auth API...\n");
  
  for (const userData of testUsers) {
    try {
      // @ts-ignore
      await auth.api.signUpEmail({
        body: userData
      });
      
      console.log(`✅ Created ${userData.role} successfully!`);
      console.log(`   Email: ${userData.email}`);
      console.log(`   Password: ${userData.password}\n`);
    } catch (err: any) {
      if (err.message?.includes("User already exists")) {
        console.log(`⚠️ User ${userData.email} already exists. Skipping.\n`);
      } else {
        console.error(`❌ Error creating ${userData.role}:`, err.message || err);
      }
    }
  }

  console.log("Done seeding users.");
  process.exit(0);
}

seedAll();
